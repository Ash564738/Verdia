# Historical PlantVillage EfficientNet-B0 Run

This report is for a previous one-epoch checkpoint only. A newer training run may
have replaced the model files. Check `models/plant_health.training.json` and
`models/plant_health.metadata.json` before associating these metrics with the
currently loaded checkpoint; rerun validation/test after the latest run completes.

Run date: 2026-11-24. PyTorch 2.11.0 CPU-only. Pretrained torchvision EfficientNet-B0, 224×224 RGB, ImageNet normalization, seed 42. Checkpoint selection used PlantVillage validation macro-F1. The test set was evaluated only after the checkpoint was frozen.

## Data used

- PlantVillage Color: official test set preserved at 10,709 images.
- Official train rows were split by group into 38,940 train and 4,338 validation after quarantining 285 rows with detected official-test group overlap and 33 exact duplicate rows. All splits contain 38 classes; no group overlap remains according to the preparation script's group IDs.
- 12,886 rows use fallback image identifiers because the upstream leaf map did not provide a leaf ID. This makes the split integrity weaker for those rows and should be documented in any report.
- Training completed one full epoch. A second epoch was requested but stopped to avoid a long CPU-only run before producing validation/test results. The retained checkpoint is the best (and only completed) validation checkpoint.

## PlantVillage results

| Split | Images | Accuracy | Macro precision | Macro recall | Macro-F1 | Weighted-F1 | Top-3 accuracy | ECE (15 bins) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Validation | 4,338 | 0.9385 | 0.9295 | 0.9128 | 0.9152 | 0.9369 | 0.9908 | 0.1071 |
| Official test | 10,709 | 0.9390 | 0.9341 | 0.9190 | 0.9233 | 0.9379 | 0.9913 | 0.1093 |

These are measured results from this one-epoch run, not a claim that proposed project targets are met. Test results were not used to tune the model. Confusion matrices and per-class metrics are in the adjacent `.validation-evaluation.json` and `.evaluation.json` files.

## PlantDoc official test

The available script used the repository's conservative label mapping, excluded 11 exact train/test duplicate images, and set the rejection threshold using only the PlantVillage validation fifth percentile. Results: 69 mapped known images, accuracy 0.1304, macro-F1 0.1748; 156 unmapped images treated as unknown; max-softmax AUROC 0.4417; unknown acceptance rate 0.2949; known rejection rate 0.7246. This is poor cross-domain/OOD performance and does not meet the proposed targets. See `models/plant_health.plantdoc-evaluation.json` and `models/plant_health.threshold.json`.

The current PlantDoc mapping is only a conservative subset, not a fully reviewed exact/verified mapping. The OOD test is limited to unmapped PlantDoc leaf classes; Cassava, Rice, and non-leaf negatives were not evaluated. Max-softmax thresholding is a baseline, not a reliable OOD guarantee.

## Artifacts

- `models/plant_health.pt`: TorchScript inference checkpoint.
- `models/plant_health.pth`: PyTorch state dict.
- `models/plant_health.labels.txt`, `models/plant_health.metadata.json`: class order and preprocessing metadata.
- `models/plant_health.training.json`: completed epoch log and early-stop status.
- `models/plant_health.validation-evaluation.json`, `models/plant_health.evaluation.json`: detailed metrics and confusion matrices.
- `models/plant_health.plantdoc-evaluation.json`, `models/plant_health.threshold.json`: cross-domain/open-set baseline.

The initial in-domain model is usable as a research baseline, but calibration and open-set performance need substantial work before deployment.

## Current EfficientNet-B0 run: 8 epochs (2026-11-24)

Checkpoint metadata confirms training used only the PlantVillage color manifest, with 38,940 training images and 4,338 validation images. Epoch 8 was selected by validation macro-F1 (0.9527). No PlantDoc images were used for training. The manifest retains the official PlantVillage test split (10,709 images), which was run once after the checkpoint was frozen.

| Evaluation split | Images | Accuracy | Macro-F1 | Top-3 | ECE |
|---|---:|---:|---:|---:|---:|
| PlantVillage official test | 10,709 | 0.9600 | 0.9510 | 0.9948 | 0.0815 |
| PlantDoc official test, verified mapped subset | 69 | 0.1884 | 0.1595 | not reported | not reported |

PlantDoc evaluation excluded 11 exact duplicates. There were 156 unmapped samples treated as unknown. Using a threshold calibrated only from PlantVillage validation (0.4736), known rejection rate was 69.6%, unknown acceptance rate 26.9%, and max-softmax AUROC 0.5059. This small mapped subset and conservative mapping limit the precision of the cross-domain estimate, but it confirms a substantial domain gap; the in-domain PlantVillage score should not be presented as expected accuracy for casual phone photos.

Current artifacts: `models/plant_health.evaluation.json` (PlantVillage official test) and `models/plant_health.plantdoc-evaluation.json` (PlantDoc official test). Do not tune the checkpoint or threshold against these test metrics.
