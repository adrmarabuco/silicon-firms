# Package Structure

- `data/`
  - corpus snapshot and preserved selection decisions
- `results/`
  - generated audit outputs used in the paper and supplement
- `scripts/`
  - scripts required to rebuild the selection and evidence artifacts

## Separation policy

This package is designed to stay close to a paper supplement / reproducibility repository.
The manuscript text can live elsewhere, but should cite the artifacts preserved here.

## Snapshot note

Until the next explicit freeze, some files here may document:

- the active strengthened corpus
- older preserved provenance freezes

That distinction should stay explicit rather than being flattened prematurely.
