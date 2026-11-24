# Label Mapping Protocol and Initial Candidates

This file is the human-review register. Similar-looking names are not proof of equivalent labels. Only rows marked `exact` or `verified` may be used in a closed-set PlantDoc benchmark. No mappings have been approved yet; the candidate rows below are deliberately `ambiguous` pending source-label semantics review.

## Required machine-readable schema

The eventual `label_mapping.yaml` must contain `dataset_name`, `original_label`, `canonical_label`, `plant_species`, `disease_name`, `mapping_status`, and `mapping_reason` for every source label. Allowed `mapping_status`: `exact`, `verified`, `ambiguous`, `unmapped`.

## Canonical label convention

Use the PlantVillage class label as the canonical identifier only after exact/verified equivalence is established. Preserve original labels verbatim. Healthy is a disease state named `healthy`. Unknown/unmapped labels remain outside the 38 known classes and are eligible only for separately reported unknown/OOD analysis.

## PlantDoc candidate crosswalk (all pending)

| PlantDoc original label | Candidate PlantVillage label | Status | Reason |
|---|---|---|---|
| Apple Scab Leaf | Apple___Apple_scab | ambiguous | Name suggests same disease; verify label scope and image semantics |
| Apple rust leaf | Apple___Cedar_apple_rust | ambiguous | Verify rust disease identity and host-specific annotation |
| Apple leaf | Apple___healthy | ambiguous | Generic label may include symptoms or unknown condition |
| Bell_pepper leaf spot | Pepper,_bell___Bacterial_spot | ambiguous | “Leaf spot” is not specific to bacterial spot |
| Bell_pepper leaf | Pepper,_bell___healthy | ambiguous | Generic label may not mean healthy |
| Blueberry leaf | — | unmapped | PV has only blueberry healthy, but label does not assert healthy |
| Cherry leaf | Cherry_(including_sour)___healthy | ambiguous | Generic leaf label; health is not explicit |
| Corn Gray leaf spot | Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot | ambiguous | Candidate semantic match, needs source annotation verification |
| Corn leaf blight | Corn_(maize)___Northern_Leaf_Blight | ambiguous | Blight subtype unspecified |
| Corn rust leaf | Corn_(maize)___Common_rust_ | ambiguous | Verify rust subtype |
| Peach leaf | Peach___healthy | ambiguous | Generic leaf label; health is not explicit |
| Potato leaf early blight | Potato___Early_blight | ambiguous | Candidate match; verify source taxonomy |
| Potato leaf late blight | Potato___Late_blight | ambiguous | Candidate match; verify source taxonomy |
| Raspberry leaf | Raspberry___healthy | ambiguous | Generic leaf label; health is not explicit |
| Soyabean leaf | Soybean___healthy | ambiguous | Crop spelling differs; health is not explicit |
| Squash Powdery mildew leaf | Squash___Powdery_mildew | ambiguous | Candidate match; verify annotation semantics |
| Strawberry leaf | Strawberry___healthy | ambiguous | Generic leaf label; health is not explicit |
| Tomato Early blight leaf | Tomato___Early_blight | ambiguous | Candidate match; verify source taxonomy |
| Tomato Septoria leaf spot | Tomato___Septoria_leaf_spot | ambiguous | Candidate match; verify annotation semantics |
| Tomato leaf | Tomato___healthy | ambiguous | Generic leaf label; health is not explicit |
| Tomato leaf bacterial spot | Tomato___Bacterial_spot | ambiguous | Candidate match; verify annotation semantics |
| Tomato leaf late blight | Tomato___Late_blight | ambiguous | Candidate match; verify annotation semantics |
| Tomato leaf mosaic virus | Tomato___Tomato_mosaic_virus | ambiguous | Candidate match; verify disease identity |
| Tomato leaf yellow virus | Tomato___Tomato_Yellow_Leaf_Curl_Virus | ambiguous | Candidate match; verify disease identity |
| Tomato mold leaf | Tomato___Leaf_Mold | ambiguous | Candidate match; verify source taxonomy |
| Tomato two spotted spider mites leaf | Tomato___Spider_mites Two-spotted_spider_mite | ambiguous | Candidate match but only two samples; verify labels |
| grape leaf | Grape___healthy | ambiguous | Generic label; health is not explicit |
| grape leaf black rot | Grape___Black_rot | ambiguous | Candidate match; verify source taxonomy |
| unclassified | — | unmapped | No reliable class label |

This candidate table is not an approved mapping. `data/dataset_audit/` records source labels and counts. Create the required YAML only after the Phase 1 label inventory is finalized and the mapping is reviewed in Phase 2.
