# Dataset Protocol

## Source policy

| Dataset | Role | Source/version | Local path | License recorded from source |
|---|---|---|---|---|
| PlantVillage Color | Primary 38-class training source and in-domain test | Git commit `7f7ecc7e1eaca78107e3affe7cb5abd9427e139a`; official split lists pinned to Hugging Face revision `9e97599868962bd0079b8db4b7f1efa9185fa1e7` | `data/plantvillage/raw/color` | CC BY-SA 3.0 in dataset card |
| PlantDoc | Cross-domain test; train portion reserved for a separate adaptation experiment | Git commit `5467f6012d78d1c446145d5f582da6096f852ae8` | `data/plantdoc/{train,test}` | CC BY 4.0 repository license |
| Cassava | OOD unknown-crop evaluation; must not be mapped into the 38 known classes | Not downloaded; source/access needs resolution | `data/cassava` (planned) | To verify before use |
| Rice | Optional OOD dataset | Not selected/downloaded | — | To verify before use |

Source licenses are recorded as metadata and must be checked against upstream terms before redistribution. PlantDoc repository README states 2,598 examples; the current pinned checkout has 2,582 train/test images plus one root-level unclassified image. This discrepancy is disclosed rather than silently filled.

## Image audit policy

1. Inventory original files and source revision before preprocessing.
2. Decode each image with Pillow; record dimensions and original mode; convert to RGB only in a derived pipeline, never overwrite source files.
3. Compute SHA-256 for exact duplicate checks. Compute perceptual hashes for near-duplicate candidates. Candidate distance is an audit heuristic and requires visual/manual review.
4. Compare duplicates across datasets and splits. Do not silently delete, relabel, or move any image.
5. Record source/license, quality state, exclusion reason, original label, canonical label and split in a manifest.
6. Keep PlantVillage RGB as the sole primary configuration. Do not count grayscale or segmented renderings of a leaf as independent samples.

## Split protocol (planned; not executed in Phase 1)

- Preserve the pinned official PlantVillage Color leaf-grouped train/test split: 43,596 train and 10,709 test.
- Carve validation only from official train with group-aware stratification after verified leaf-group IDs and duplicate findings are available. No official test use for model selection.
- PlantDoc official test remains untouched for cross-domain evaluation. Its train data may only enter the separate domain-adaptation experiment after its independent validation subset is defined.
- Unknown crop/disease OOD calibration and OOD test sets must be disjoint. OOD test cannot select thresholds.
- Every split must have assertions for image coverage, group disjointness, exact/near duplicate leakage, and label counts before training is permitted.

## Manifest contract

The target manifest columns are `image_id,image_path,dataset,source_version,original_label,canonical_label,plant,disease,class_index,group_id,sha256,perceptual_hash,split,license,quality_status,exclude_reason`. Missing values remain explicit; class indices must come from a reviewed mapping file, never folder order or alphabetical order. Phase 1 manifests may leave canonical labels, class index, group ID, or pHash unset until the corresponding checks are completed.

## Phase gate

No training starts until Phase 1 audit evidence is reviewed and Phase 2 mapping/split integrity checks pass. The user must explicitly approve moving to Phase 2.
