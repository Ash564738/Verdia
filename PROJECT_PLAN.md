# Smart Plant Care AI — Project Plan

## Scope

This work follows the user's phase gate: dataset engineering and the AI core only. Frontend, website deployment, and mobile deployment are out of scope. Training must not begin before the Phase 1 audit and Phase 2 split integrity checks pass. Moving past Phase 1 requires explicit user approval.

## Phases and gates

| Phase | Work | Exit evidence | State |
|---|---|---|---|
| 1. Dataset download and audit | Pin sources; recover/download datasets; inventory, decode/quality, hashes, duplicate and license audit | `DATASET_AUDIT.md`, manifests, source revisions, duplicate reports, OOD data availability | In progress: PlantVillage and PlantDoc audited; Cassava source acquisition unresolved |
| 2. Harmonization and split generation | Review mapping; preserve official PV split; generate group-aware PV validation; define independent calibration/OOD partitions | Reviewed mapping; leakage/coverage assertions pass | Not started; requires approval after Phase 1 |
| 3. EDA and preprocessing | EDA notebooks and deterministic preprocessing specification | Notebooks and reports | Not started |
| 4. CNN baseline | Reproducible training and validation selection | Checkpoint and validation metrics | Not started |
| 5. EfficientNet-B0 | Transfer learning and validation selection | Checkpoint and validation comparison | Not started |
| 6. Internal evaluation | One-time frozen evaluation on official PlantVillage test | Full metrics and uncertainty reports | Not started |
| 7. PlantDoc cross-domain | Evaluate only reviewed exact/verified common labels | Frozen cross-domain report | Not started |
| 8. OOD evaluation | Calibration and independent open-set test | OOD metrics at declared operating point | Not started |
| 9. Model finalization and AI backend | Freeze model; implement FastAPI inference modules and automated tests | Model metadata, API, tests, operational docs | Not started |

## Phase 1 findings

- PlantVillage Color: 54,305 valid images across 38 labels; source revision and official split list are recorded in `DATASET_AUDIT.md`.
- PlantDoc: 2,582 images in the repository's train/test directories (2,346/236) and one additional unclassified image at repository root; 28 train labels and 27 test labels.
- Both sources have zero decode failures in the current audit. Exact duplicates and perceptual near-duplicate candidates are reported for review; no image is deleted or excluded automatically.
- Cassava is not present locally and its acquisition source/access/license still needs resolution. Rice is optional and has not been added.
- No training or new validation split was performed for this phase.

## Current gate

The pHash report is complete. Phase 1 remains open because Cassava has not been acquired and its source access/license are unresolved. Provide the current audit evidence for review and wait for explicit approval before Phase 2.
