# Building AI-Based Information Systems

# Automatic and Semi-Automatic Data Anonymization

## Project Overview

This project focuses on the automatic and semi-automatic anonymization of
structured and unstructured data before it is made available to downstream
AI-based information systems.

The main objective is to detect Personally Identifiable Information (PII),
apply appropriate anonymization techniques, and evaluate different detection
approaches on a shared synthetic dataset.

The project currently focuses on tabular medical data and combines
deterministic rule-based detection with AI-based Named Entity Recognition
(NER) approaches.

---

## Project Goals

The main goals of the project are:

- Normalize input data into a common representation.
- Detect PII in structured and free-text data.
- Apply different anonymization techniques depending on the type of PII.
- Compare multiple PII detection approaches using a common interface.
- Evaluate detection quality using reproducible metrics.
- Compare approaches in terms of accuracy, runtime, and resource usage.
- Identify the most suitable approach or combination of approaches for the
  target data.

---

## Current Data

The current application dataset is a synthetic diabetology dataset stored in
Excel format.

The dataset contains fields including:

- Patient Code
- First Name
- Surname
- Tax Code
- Birth Date
- Assessment Date
- Age At Assessment

No real personal data is used in the evaluation.

---

## Current Architecture

The current pipeline is:

    Input file
        ↓
    Universal loader
        ↓
    Normalized data
        ↓
    PII detection
        ↓
    Anonymization
        ↓
    Anonymized output

The detection component currently includes:

    PII Detection
        ├── Rule-based / Regex
        ├── spaCy NER
        ├── Hugging Face NER
        └── GLiNER

The AI-based detectors use a common `Detector` interface so that they can be
evaluated through the same pipeline.

---

## Anonymization Methods

Different PII fields currently use different anonymization strategies.

| PII Field | Method |
|---|---|
| Patient Code | Pseudonymization |
| First Name | Masking |
| Surname | Masking |
| Tax Code | Masking |
| Birth Date | Generalization |
| Assessment Date | Generalization |
| Age At Assessment | Generalization |

For example, patient codes are converted into consistent pseudonyms such as:

    PATIENT_0001

Age is generalized into ranges such as:

    70-79

Dates are generalized to preserve useful information while reducing the
amount of identifying information retained.

---

## AI-Based PII Detection

Three AI-based approaches are currently implemented:

### spaCy

spaCy NER models are used for named entity detection. Both English and
Italian models are currently used.

### Hugging Face

A multilingual transformer-based NER model is used for contextual entity
detection.

### GLiNER

GLiNER is used as a flexible NER approach where entity categories can be
specified for the detection task.

All three approaches produce a common detection format and can therefore be
evaluated using the same benchmark.

---

## Evaluation

A manually annotated ground-truth dataset has been created for evaluating the
AI-based detectors.

The evaluation dataset currently contains English and Italian examples
covering entities such as:

- Persons
- Locations
- Organizations
- Dates

The ground truth uses character-level entity spans (`start` and `end`
positions). The detectors also return predicted entity spans, allowing the
evaluation to compare both the entity type and its exact position in the text.

The current evaluation uses:

- True Positive (TP)
- False Positive (FP)
- False Negative (FN)
- Precision
- Recall
- F1-score

### Current Results

| Detector | Precision | Recall | F1 |
|---|---:|---:|---:|
| spaCy | 0.661 | 0.860 | 0.747 |
| Hugging Face | 0.897 | 0.814 | 0.854 |
| GLiNER | 0.976 | 0.953 | **0.965** |

On the current evaluation dataset, GLiNER achieves the highest F1-score.

These results are preliminary and will be complemented by runtime,
memory/resource measurements, and detailed error analysis.

---

## Repository Structure

The project is currently organized approximately as follows:

    src/
    ├── normalization/
    ├── detection/
    ├── anonymization/
    └── evaluation/

    data/
    output/

The detection module contains the different PII detection approaches, while
the anonymization module contains the rule-based anonymization logic.
Evaluation contains the ground truth and detector benchmarking code.

---

## How to Run

Set the Python path to the `src` directory:

    $env:PYTHONPATH="src"

Run the main anonymization pipeline:

    py -3.11 src/main.py

The anonymized dataset is written to:

    output/anonymized_dataset.xlsx

To run the detector evaluation:

    py -3.11 -m evaluation.evaluation

---

## Current Status

### Completed

- [x] Universal data loading / normalization
- [x] Rule-based PII detection
- [x] Rule-based anonymization
- [x] Patient-code pseudonymization
- [x] Name and tax-code masking
- [x] Date and age generalization
- [x] spaCy NER detector
- [x] Hugging Face NER detector
- [x] GLiNER detector
- [x] Common detector interface
- [x] Ground-truth evaluation dataset
- [x] TP / FP / FN evaluation
- [x] Precision / Recall / F1 evaluation
- [x] Character-level span evaluation
- [x] Initial comparison of the three AI-based detectors

### Next Steps

- [ ] Runtime / inference-time benchmarking
- [ ] Model loading-time comparison
- [ ] Memory and resource-usage comparison
- [ ] Detailed false-positive and false-negative analysis
- [ ] Expand the evaluation dataset
- [ ] Qualitative comparison of anonymization outputs
- [ ] Final detector / hybrid strategy selection
- [ ] Further integration and reproducibility work
- [ ] Docker / Docker Compose deployment

---

## Progress Log

### 2026-08-08

- Added Hugging Face NER as an additional AI-based PII detector.
- Added GLiNER as a third AI-based detector.
- Introduced a common detector interface.
- Created a ground-truth dataset for detector evaluation.
- Implemented TP, FP, FN, Precision, Recall, and F1-score.
- Extended evaluation to use character-level entity spans.
- Updated detectors to return predicted entity spans.
- Performed the initial comparison of spaCy, Hugging Face, and GLiNER.
- GLiNER currently achieved the highest F1-score on the evaluation dataset.