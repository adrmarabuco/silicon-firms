#!/usr/bin/env python3
"""
Build an auditable master selection table for the survey corpus.

Sources:
- data/selection.csv
- data/decisions/direct_import_log.csv
- latest data/decisions/snowballing_log*.csv snapshot
- papers.json

Outputs:
- results/master_selection_table.csv
- results/master_selection_summary.md
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELECTION_CSV = ROOT / "data" / "selection.csv"
DECISIONS_DIR = ROOT / "data" / "decisions"
DIRECT_IMPORT_CSV = DECISIONS_DIR / "direct_import_log.csv"
PAPERS_JSON = ROOT / "papers.json"
OUTPUT_CSV = ROOT / "results" / "master_selection_table.csv"
OUTPUT_MD = ROOT / "results" / "master_selection_summary.md"


def normalize_title(text: str | None) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def normalize_url(url: str | None) -> str:
    if not url:
        return ""
    url = url.strip()
    if not re.match(r"^https?://", url, flags=re.IGNORECASE):
        return ""
    url = url.replace("http://", "https://")
    return url.rstrip("/").lower()


def slugify(text: str | None) -> str:
    text = normalize_title(text)
    if not text:
        return "untitled"
    return re.sub(r"\s+", "-", text)[:80]


def extract_ids(value: str | None) -> list[str]:
    ids: list[str] = []
    if not value:
        return ids

    text = value.strip()
    lower = text.lower().strip()
    normalized_url = normalize_url(text)

    if normalized_url.startswith("https://"):
        ids.append(f"url:{normalized_url}")

    arxiv_matches = re.findall(
        r"(?:arxiv:|arxiv\.org/(?:abs|pdf)/)([0-9]{4}\.[0-9]{4,5})(?:v\d+)?",
        lower,
    )
    for match in arxiv_matches:
        ids.append(f"arxiv:{match}")

    doi_matches = re.findall(r"(10\.\d{4,9}/[^\s?#]+)", lower)
    for match in doi_matches:
        ids.append(f"doi:{match.rstrip('/').lower()}")

    if "aclanthology.org/" in normalized_url:
        suffix = normalized_url.split("aclanthology.org/", 1)[1]
        ids.append(f"aclan:{suffix}")
        ids.append(f"doi:10.18653/v1/{suffix}")

    seen = set()
    deduped = []
    for item in ids:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def latest_snowball_log() -> Path:
    round_logs = sorted(DECISIONS_DIR.glob("snowballing_log.forward-*.round-*.csv"))
    if round_logs:
        return round_logs[-1]
    fallback = DECISIONS_DIR / "snowballing_log.csv"
    if fallback.exists():
        return fallback
    raise FileNotFoundError("No snowballing log found.")


def ensure_record(records: dict[str, dict], aliases: dict[str, str], keys: list[str]) -> dict:
    existing_ids = []
    for key in keys:
        if key in aliases and aliases[key] not in existing_ids:
            existing_ids.append(aliases[key])

    if not existing_ids:
        next_index = len(records) + 1
        existing = f"cand:{next_index:04d}"
        while existing in records:
            next_index += 1
            existing = f"cand:{next_index:04d}"
        records[existing] = {
            "title": "",
            "normalized_title": "",
            "year": "",
            "authors": "",
            "venue": "",
            "canonical_url": "",
            "canonical_ids": set(),
            "source_pathways": set(),
            "source_names": set(),
            "selection_searches": set(),
            "selection_decisions": set(),
            "selection_rows": 0,
            "snowball_directions": set(),
            "snowball_decisions": set(),
            "snowball_seed_record_ids": set(),
            "snowball_reasons": set(),
            "snowball_rows": 0,
            "included_final": False,
            "linked_record_id": "",
            "reconciliation_status": "",
            "primary_pathway": "",
        }
    else:
        def score(record_id: str) -> tuple[int, int, int]:
            rec = records[record_id]
            return (
                1 if rec["linked_record_id"] else 0,
                1 if rec["included_final"] else 0,
                rec["selection_rows"] + rec["snowball_rows"],
            )

        existing = max(existing_ids, key=score)
        for other_id in existing_ids:
            if other_id == existing:
                continue
            merge_records(records, aliases, existing, other_id)

    for key in keys:
        aliases[key] = existing
    return records[existing]


def merge_records(records: dict[str, dict], aliases: dict[str, str], target_id: str, source_id: str) -> None:
    if target_id == source_id or source_id not in records:
        return

    target = records[target_id]
    source = records[source_id]

    for field in ("title", "normalized_title", "year", "authors", "venue", "canonical_url", "linked_record_id"):
        if not target[field] and source[field]:
            target[field] = source[field]

    for field in (
        "canonical_ids",
        "source_pathways",
        "source_names",
        "selection_searches",
        "selection_decisions",
        "snowball_directions",
        "snowball_decisions",
        "snowball_seed_record_ids",
        "snowball_reasons",
    ):
        target[field].update(source[field])

    target["selection_rows"] += source["selection_rows"]
    target["snowball_rows"] += source["snowball_rows"]
    target["included_final"] = target["included_final"] or source["included_final"]

    for alias, record_id in list(aliases.items()):
        if record_id == source_id:
            aliases[alias] = target_id

    del records[source_id]


def choose_uid(record: dict) -> str:
    if record["linked_record_id"]:
        return record["linked_record_id"]

    for prefix in ("doi:", "arxiv:", "aclan:"):
        for item in sorted(record["canonical_ids"]):
            if item.startswith(prefix):
                return item.upper().replace(":", "_", 1).replace("/", "_")

    if record["canonical_url"]:
        digest = hashlib.sha1(record["canonical_url"].encode()).hexdigest()[:10]
        return f"URL_{digest}"

    return f"CAND_{slugify(record['title'])}"


def infer_primary_pathway(record: dict) -> str:
    pathways = record["source_pathways"]
    if "direct_import" in pathways and len(pathways) == 1:
        return "direct_import"
    if "direct_import" in pathways:
        return "mixed+direct_import"
    if "seeded_search" in pathways and "snowballing" in pathways:
        return "seeded_search+snowballing"
    if "seeded_search" in pathways:
        return "seeded_search"
    if "snowballing" in pathways:
        return "snowballing"
    if record["included_final"]:
        return "included_snapshot_only"
    return "unknown"


def infer_reconciliation_status(record: dict) -> str:
    seeded = "seeded_search" in record["source_pathways"]
    snow = "snowballing" in record["source_pathways"]
    direct = "direct_import" in record["source_pathways"]
    included = record["included_final"]

    if included and seeded and snow:
        return "included_reconciled_both"
    if included and direct:
        return "included_reconciled_direct_import"
    if included and seeded:
        return "included_reconciled_seeded_search"
    if included and snow:
        return "included_reconciled_snowballing"
    if included:
        return "included_unreconciled_in_snapshot"

    decisions = record["snowball_decisions"]
    reasons = " ".join(sorted(record["snowball_reasons"])).lower()
    if "include" in decisions and "duplicate" in reasons:
        return "screened_duplicate_version"
    if "pending" in decisions:
        return "screened_pending"
    if "exclude" in decisions and decisions <= {"exclude"}:
        return "screened_excluded"
    if "include" in decisions:
        return "screened_include_not_imported"
    return "screened_other"


def main() -> None:
    snowball_csv = latest_snowball_log()
    records: dict[str, dict] = {}
    aliases: dict[str, str] = {}

    selection_rows = list(csv.DictReader(SELECTION_CSV.open()))
    for row in selection_rows:
        keys = [f"title:{normalize_title(row.get('Title'))}"]
        keys.extend(extract_ids(row.get("Link")))
        record = ensure_record(records, aliases, [k for k in keys if k and k != "title:"])
        record["title"] = record["title"] or (row.get("Title") or "").strip()
        record["normalized_title"] = record["normalized_title"] or normalize_title(row.get("Title"))
        record["authors"] = record["authors"] or (row.get("Authors") or "").strip()
        record["canonical_url"] = record["canonical_url"] or normalize_url(row.get("Link"))
        record["canonical_ids"].update(extract_ids(row.get("Link")))
        record["source_pathways"].add("seeded_search")
        record["source_names"].add((row.get("Source") or "").strip() or (row.get("Search") or "").strip())
        record["selection_searches"].add((row.get("Search") or "").strip())
        record["selection_decisions"].add((row.get("Rejeitado") or "").strip())
        record["selection_rows"] += 1

    if DIRECT_IMPORT_CSV.exists():
        direct_rows = list(csv.DictReader(DIRECT_IMPORT_CSV.open()))
        for row in direct_rows:
            keys = [f"record:{(row.get('record_id') or '').strip()}"]
            keys.append(f"title:{normalize_title(row.get('title'))}")
            keys.extend(extract_ids(row.get("url")))
            keys = [k for k in keys if k and k != "title:"]
            if not keys:
                continue

            record = ensure_record(records, aliases, keys)
            record["title"] = record["title"] or (row.get("title") or "").strip()
            record["normalized_title"] = record["normalized_title"] or normalize_title(row.get("title"))
            record["year"] = record["year"] or (row.get("year") or "").strip()
            record["authors"] = record["authors"] or (row.get("authors") or "").strip()
            record["venue"] = record["venue"] or (row.get("venue") or "").strip()
            record["canonical_url"] = record["canonical_url"] or normalize_url(row.get("url"))
            record["canonical_ids"].update(extract_ids(row.get("url")))
            record["source_pathways"].add("direct_import")
            record["source_names"].add((row.get("source_name") or "").strip() or "direct_import")

    snowball_rows = list(csv.DictReader(snowball_csv.open()))
    for row in snowball_rows:
        keys = []
        reason = (row.get("reason") or "").strip()
        imported_match = re.search(r"\bImported as (A\d{3})\b", reason)
        if imported_match:
            keys.append(f"record:{imported_match.group(1)}")
        if row.get("candidate_title"):
            keys.append(f"title:{normalize_title(row.get('candidate_title'))}")
        id_value = row.get("candidate_id_value")
        id_type = (row.get("candidate_id_type") or "").strip().lower()
        if id_value:
            if id_type == "arxiv":
                keys.extend(extract_ids(f"arXiv:{id_value}"))
            else:
                keys.extend(extract_ids(id_value))
        keys.extend(extract_ids(row.get("candidate_url")))
        keys = [k for k in keys if k]
        if not keys:
            continue

        record = ensure_record(records, aliases, keys)
        if row.get("candidate_title"):
            record["title"] = record["title"] or row["candidate_title"].strip()
            record["normalized_title"] = record["normalized_title"] or normalize_title(row["candidate_title"])
        record["year"] = record["year"] or (row.get("candidate_year") or "").strip()
        record["authors"] = record["authors"] or (row.get("candidate_authors") or "").strip()
        record["venue"] = record["venue"] or (row.get("candidate_venue") or "").strip()
        record["canonical_url"] = record["canonical_url"] or normalize_url(row.get("candidate_url"))
        record["canonical_ids"].update(extract_ids(row.get("candidate_id_value")))
        record["canonical_ids"].update(extract_ids(row.get("candidate_url")))
        record["source_pathways"].add("snowballing")
        record["source_names"].add("snowballing")
        record["snowball_directions"].add((row.get("direction") or "").strip())
        record["snowball_decisions"].add((row.get("decision") or "").strip())
        record["snowball_seed_record_ids"].add((row.get("seed_record_id") or "").strip())
        if reason:
            record["snowball_reasons"].add(reason)
        record["snowball_rows"] += 1

    papers = json.loads(PAPERS_JSON.read_text())
    for rec in papers:
        bib = rec["bibliographic"]
        keys = [f"record:{bib.get('record_id')}", f"title:{normalize_title(bib.get('title'))}"]
        keys.extend(extract_ids(bib.get("url")))
        keys = [k for k in keys if k and k != "title:"]
        record = ensure_record(records, aliases, keys)
        record["title"] = record["title"] or (bib.get("title") or "").strip()
        record["normalized_title"] = record["normalized_title"] or normalize_title(bib.get("title"))
        record["year"] = record["year"] or str(bib.get("year") or "").strip()
        authors = bib.get("authors") or []
        if isinstance(authors, list):
            authors = "; ".join(authors)
        record["authors"] = record["authors"] or str(authors).strip()
        record["venue"] = record["venue"] or str(bib.get("venue") or "").strip()
        record["canonical_url"] = record["canonical_url"] or normalize_url(bib.get("url"))
        record["canonical_ids"].update(extract_ids(bib.get("url")))
        record["included_final"] = True
        if not record["linked_record_id"] or record["linked_record_id"] == (bib.get("record_id") or ""):
            record["linked_record_id"] = bib.get("record_id") or ""

    output_rows = []
    for record in records.values():
        record["primary_pathway"] = infer_primary_pathway(record)
        record["reconciliation_status"] = infer_reconciliation_status(record)
        output_rows.append(
            {
                "candidate_uid": choose_uid(record),
                "title": record["title"],
                "year": record["year"],
                "authors": record["authors"],
                "venue": record["venue"],
                "canonical_url": record["canonical_url"],
                "canonical_ids": " | ".join(sorted(record["canonical_ids"])),
                "source_pathways": " | ".join(sorted(p for p in record["source_pathways"] if p)),
                "source_names": " | ".join(sorted(s for s in record["source_names"] if s)),
                "selection_searches": " | ".join(sorted(s for s in record["selection_searches"] if s)),
                "selection_decisions": " | ".join(sorted(s for s in record["selection_decisions"] if s)),
                "selection_rows": record["selection_rows"],
                "snowball_directions": " | ".join(sorted(s for s in record["snowball_directions"] if s)),
                "snowball_decisions": " | ".join(sorted(s for s in record["snowball_decisions"] if s)),
                "snowball_seed_record_ids": " | ".join(sorted(s for s in record["snowball_seed_record_ids"] if s)),
                "snowball_rows": record["snowball_rows"],
                "snowball_reason_samples": " | ".join(sorted(s for s in list(record["snowball_reasons"])[:5] if s)),
                "included_final": "yes" if record["included_final"] else "no",
                "linked_record_id": record["linked_record_id"],
                "primary_pathway": record["primary_pathway"],
                "reconciliation_status": record["reconciliation_status"],
            }
        )

    output_rows.sort(
        key=lambda row: (
            row["linked_record_id"] == "",
            row["linked_record_id"],
            row["title"].lower(),
        )
    )

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(output_rows[0].keys()))
        writer.writeheader()
        writer.writerows(output_rows)

    status_counts = Counter(row["reconciliation_status"] for row in output_rows)
    pathway_counts = Counter(row["primary_pathway"] for row in output_rows)
    included_count = sum(1 for row in output_rows if row["included_final"] == "yes")
    pending_count = sum(1 for row in output_rows if row["reconciliation_status"] == "screened_pending")
    excluded_count = sum(1 for row in output_rows if row["reconciliation_status"] == "screened_excluded")
    unresolved_include_count = sum(
        1 for row in output_rows if row["reconciliation_status"] == "screened_include_not_imported"
    )

    lines = [
        "# Master Selection Table Summary",
        "",
        f"- Generated from `{SELECTION_CSV.relative_to(ROOT)}`, `{DIRECT_IMPORT_CSV.relative_to(ROOT)}`, `{snowball_csv.relative_to(ROOT)}`, and `{PAPERS_JSON.relative_to(ROOT)}`.",
        f"- Unique candidate rows after reconciliation: `{len(output_rows)}`.",
        f"- Final included studies linked to `papers.json`: `{included_count}`.",
        f"- Pending screened candidates: `{pending_count}`.",
        f"- Excluded screened candidates: `{excluded_count}`.",
        f"- Snowball `include` decisions not yet linked to the final corpus snapshot: `{unresolved_include_count}`.",
        "",
        "## Reconciliation Status Counts",
        "",
    ]
    for key, value in sorted(status_counts.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Primary Pathway Counts", ""])
    for key, value in sorted(pathway_counts.items()):
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `included_unreconciled_in_snapshot` means the paper exists in `papers.json`, but this repository snapshot does not yet preserve a matching search or snowballing event for it.",
            "- `screened_include_not_imported` usually indicates a duplicate, a related version, or a candidate marked `include` in the snowballing snapshot without a direct final linkage.",
            "- This table is audit-oriented: it favors preserving provenance over forcing a cleaner but less defensible PRISMA count.",
        ]
    )

    OUTPUT_MD.write_text("\n".join(lines) + "\n")

    print(f"Wrote {OUTPUT_CSV.relative_to(ROOT)}")
    print(f"Wrote {OUTPUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
