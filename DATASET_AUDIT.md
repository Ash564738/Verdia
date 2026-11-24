# Phase 1 Dataset Audit

Audit date: 2026-11-24 (Asia/Bangkok). This is an inventory and quality audit, not model evaluation. No training was started and no source image was automatically excluded.

## Summary

| Dataset | Source revision | Images | Labels | Decode failures | Notes |
|---|---|---:|---:|---:|---|
| PlantVillage Color | Git `7f7ecc7e1eaca78107e3affe7cb5abd9427e139a`; split lists at HF revision `9e97599868962bd0079b8db4b7f1efa9185fa1e7` | 54,305 | 38 | 0 | All 256×256; 54,304 RGB and 1 RGBA |
| PlantDoc train/test | Git `5467f6012d78d1c446145d5f582da6096f852ae8` | 2,582 in official directories, plus 1 root-level unclassified image in checkout | 28 train / 27 test; 29 labels including root image | 0 | Train 2,346; test 236; mixed sizes and modes |
| Cassava OOD | Not acquired | 0 | 0 | — | Not in workspace. TFDS catalog describes 9,430 images across 5 classes, but access/source package and applicable image license must be verified before use. |

PlantVillage official split coverage: 43,596 train + 10,709 test = 54,305. The pinned split inventory is checked for exact local coverage in `scripts/audit_perceptual_hashes.py`. The earlier exact-hash audit found 21 duplicate groups within PlantVillage, 0 exact cross-split duplicate groups, and 0 exact cross-dataset matches. Groups require investigation; this does not certify leaf-group integrity by itself.

PlantDoc class count discrepancy: upstream README states 2,598 examples, while this pinned checkout has 2,582 images under train/test plus one image under an unclassified root location. The current checkout is audited as it exists; the discrepancy is not silently reconciled. There are 11 exact duplicate groups crossing PlantDoc train/test, which must be reviewed before any evaluation claims. No cross-dataset exact duplicate with PlantVillage was found.

## PlantVillage Color class distribution

| Original class label | Count |
|---|---:|
| Apple___Apple_scab | 630 |
| Apple___Black_rot | 621 |
| Apple___Cedar_apple_rust | 275 |
| Apple___healthy | 1,645 |
| Blueberry___healthy | 1,502 |
| Cherry_(including_sour)___Powdery_mildew | 1,052 |
| Cherry_(including_sour)___healthy | 854 |
| Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot | 513 |
| Corn_(maize)___Common_rust_ | 1,192 |
| Corn_(maize)___Northern_Leaf_Blight | 985 |
| Corn_(maize)___healthy | 1,162 |
| Grape___Black_rot | 1,180 |
| Grape___Esca_(Black_Measles) | 1,383 |
| Grape___Leaf_blight_(Isariopsis_Leaf_Spot) | 1,076 |
| Grape___healthy | 423 |
| Orange___Haunglongbing_(Citrus_greening) | 5,507 |
| Peach___Bacterial_spot | 2,297 |
| Peach___healthy | 360 |
| Pepper,_bell___Bacterial_spot | 997 |
| Pepper,_bell___healthy | 1,478 |
| Potato___Early_blight | 1,000 |
| Potato___Late_blight | 1,000 |
| Potato___healthy | 152 |
| Raspberry___healthy | 371 |
| Soybean___healthy | 5,090 |
| Squash___Powdery_mildew | 1,835 |
| Strawberry___Leaf_scorch | 1,109 |
| Strawberry___healthy | 456 |
| Tomato___Bacterial_spot | 2,127 |
| Tomato___Early_blight | 1,000 |
| Tomato___Late_blight | 1,909 |
| Tomato___Leaf_Mold | 952 |
| Tomato___Septoria_leaf_spot | 1,771 |
| Tomato___Spider_mites Two-spotted_spider_mite | 1,676 |
| Tomato___Target_Spot | 1,404 |
| Tomato___Tomato_Yellow_Leaf_Curl_Virus | 5,357 |
| Tomato___Tomato_mosaic_virus | 373 |
| Tomato___healthy | 1,591 |

Counts range from 152 (Potato healthy) to 5,507 (Orange greening), so imbalance is substantial and must be considered using training-only weighting/sampling if needed.

## PlantDoc distribution by label

Counts below combine the repository's train and test directories. See `data/dataset_audit/dataset_audit.json` and `plantdoc_manifest.csv` for per-image details. The train/test distribution is deliberately not used for model selection.

| Original label | Count | Original label | Count |
|---|---:|---|---:|
| Apple Scab Leaf | 93 | Apple leaf | 92 |
| Apple rust leaf | 89 | Bell_pepper leaf | 61 |
| Bell_pepper leaf spot | 71 | Blueberry leaf | 118 |
| Cherry leaf | 58 | Corn Gray leaf spot | 68 |
| Corn leaf blight | 192 | Corn rust leaf | 116 |
| Peach leaf | 112 | Potato leaf early blight | 117 |
| Potato leaf late blight | 105 | Raspberry leaf | 119 |
| Soyabean leaf | 65 | Squash Powdery mildew leaf | 130 |
| Strawberry leaf | 96 | Tomato Early blight leaf | 88 |
| Tomato Septoria leaf spot | 151 | Tomato leaf | 63 |
| Tomato leaf bacterial spot | 110 | Tomato leaf late blight | 111 |
| Tomato leaf mosaic virus | 54 | Tomato leaf yellow virus | 76 |
| Tomato mold leaf | 91 | Tomato two spotted spider mites leaf | 2 |
| grape leaf | 70 | grape leaf black rot | 64 |
| unclassified (repository root) | 1 | | |

Image modes: 2,571 RGB, 6 RGBA, 1 grayscale (`L`), 5 CMYK. The audit converts these only for derived processing; originals remain unchanged. Dimensions vary widely; the 20 most common dimensions are in the JSON audit.

## Near duplicates and exclusions

Exact duplicate audit artifacts: `data/dataset_audit/dataset_audit.json`, `plantvillage_manifest.csv`, and `plantdoc_manifest.csv`. pHash audit completed via `scripts/audit_perceptual_hashes.py`; it found 1,403 candidate pairs at Hamming distance ≤4, of which 410 cross a split within the same dataset and 1 crosses dataset boundaries. The cross-dataset candidate is not an exact SHA match (distance 4; PlantVillage Apple healthy vs PlantDoc Tomato late blight) and requires visual review. PlantDoc's 11 exact cross-split groups are among the candidates and must be investigated. PlantVillage official split coverage passed exactly. The configured Hamming distance is for candidate discovery only; no candidate was auto-excluded.

Current corrupt/invalid image count: 0 for both downloaded sources. This finding is limited to the current source checkouts and the image decoder/audit used.

## Acquisition and provenance limits

- PlantVillage dataset card declares CC BY-SA 3.0. PlantDoc repository license is CC BY 4.0. Preserve attribution and source revisions.
- TFDS catalogs Cassava as 9,430 labeled samples in five classes and a 1.26 GiB source, citing the Kaggle Cassava competition. The project workspace has no Cassava files or Kaggle CLI credential. TFDS also cautions that it does not grant dataset rights; verify source terms and obtain data before OOD evaluation. [TFDS Cassava catalog](https://www.tensorflow.org/datasets/catalog/cassava), [TFDS data access and licensing note](https://github.com/tensorflow/datasets).
- Rice is optional, not selected, and not downloaded.
- Training hardware currently reports PyTorch 2.11.0 CPU-only (`torch.cuda.is_available() == False`). This is a compute constraint, not a dataset integrity failure.

## Phase 1 exit status

**Not yet complete.** pHash candidate generation and official PlantVillage split coverage completed. Cassava acquisition/provenance still needs resolution, and duplicate candidates require review before benchmark preparation. No split generation or training is authorized until this report is reviewed and the user explicitly approves Phase 2.
