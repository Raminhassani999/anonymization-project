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

## Current Evaluation

## Current Evaluation

Three AI-based PII detection approaches are currently implemented:

- spaCy
- Hugging Face NER
- GLiNER

All detectors use a common interface and are evaluated against the same
synthetic ground-truth dataset.

The benchmark contains **36 text examples** and **97 annotated PII entities**,
covering both structured records and free-text examples in English and Italian.

### Detection Results

Detection Results

The current detection benchmark evaluates exact entity spans and normalized
entity types using:

True Positives (TP)
False Positives (FP)
False Negatives (FN)
Precision
Recall
F1-score
Overall
Detector	Precision	Recall	F1
spaCy	0.441	0.691	0.538
Hugging Face	0.860	0.763	0.809
GLiNER	0.922	0.969	0.945

GLiNER currently provides the strongest overall detection performance on the
evaluation dataset.

Structured Text
Detector	Precision	Recall	F1
spaCy	0.323	0.574	0.413
Hugging Face	0.809	0.704	0.752
GLiNER	0.867	0.963	0.912
Free Text
Detector	Precision	Recall	F1
spaCy	0.643	0.837	0.727
Hugging Face	0.923	0.837	0.878
GLiNER	1.000	0.977	0.988

GLiNER performs particularly strongly on free-text examples, achieving an F1
score of 0.988.

Performance Results

The performance benchmark currently uses 36 synthetic text examples.

Detector	Loading Time (s)	Inference / Example (s)	Memory After Loading (MB)	Memory After Inference (MB)
spaCy	2.3982	0.006942	329.36	330.72
Hugging Face	4.8767	0.024776	396.61	1045.12
GLiNER	5.0755	0.057249	418.42	1231.18

spaCy is currently the fastest and most memory-efficient approach in the
benchmark.

GLiNER requires more computational resources and has the highest inference
time and memory consumption, but provides substantially stronger detection
accuracy.

### Structured vs. Free-Text Results

The benchmark separates structured-style examples from free-text examples
to evaluate whether detection performance changes depending on the input
format.

| Detector     | Structured F1 | Free-Text F1 |
| ------------ | ------------: | -----------: |
| spaCy        | 0.440 | 0.747 |
| Hugging Face | 0.713 | 0.854 |
| GLiNER       | **0.877** | **0.965** |

All three detectors currently perform better on free-text examples than on
structured-style examples.

GLiNER achieves the strongest performance in both categories, while spaCy
shows the largest performance difference between structured-style and
free-text inputs.

### End-to-End Anonymization

A rule-based text anonymization layer was implemented to transform detected
entities into anonymized placeholders:

Entity Type	Replacement
person	[PERSON]
organization	[ORGANIZATION]
location	[LOCATION]
date	[DATE]
misc	[MISC]

The text anonymizer applies replacements from right to left so that character
offsets remain valid when multiple entities are anonymized in the same text.

The anonymization component has been tested independently with 5/5 passing
tests.

The existing DataFrame-based rule anonymizer has also been tested with
9/9 passing tests.


### End-to-End Results

The end-to-end benchmark evaluates the output produced after passing detector
predictions through the text anonymization layer.

| Detector     | Exact Output Match | Remaining PII |
|--------------|-------------------:|--------------:|
| spaCy        | 2.8%               | 0 |
| Hugging Face | 52.8%              | 2 |
| GLiNER       | **80.6%**           | **0** |

GLiNER currently provides the strongest end-to-end anonymization performance,
with **29 of 36 examples producing an exact match with the expected anonymized
output**.

The benchmark also reports an entity-level rate of 96.9% for GLiNER. This
corresponds to the detector's entity recall under the current evaluation
definition and is therefore not treated as an independent anonymization
metric.

The **exact output match rate** is used as the primary end-to-end
anonymization quality indicator.



### Error Analysis

The benchmark includes diagnostic analysis of:

False positives
False negatives
Entity-boundary errors
Entity-type errors

The analysis shows that:

spaCy produces substantially more false positives and entity-type and
boundary errors, particularly on structured examples.
Hugging Face provides stronger precision than spaCy but still misses
several entities, including date and location entities.
GLiNER produces substantially fewer errors overall. Its remaining errors
are mainly associated with specific location entities and structured-text
boundary or entity interpretation cases.

### Structured Input Considerations

The structured-style benchmark represents PII using key-value-like text
fields, such as `Name`, `City`, `Hospital`, and `Date`.

These field labels are not annotated as PII. Predictions over field labels are
therefore counted as false positives. This tests whether a detector can
distinguish between schema labels and the actual PII values contained in the
input.

### Current Benchmark Summary

The current benchmark contains:

- **36 synthetic text examples**
- **18 free-text examples**
- **18 structured-style examples**
- **97 annotated PII entities**

The benchmark currently evaluates:

- Detection accuracy
- Precision, Recall, and F1-score
- Structured vs. free-text performance
- Model loading time
- Inference time
- Memory usage
- False-positive analysis
- False-negative analysis
- Entity-boundary errors
- Entity-type errors
- Ground-truth span validity

All 97 ground-truth entities currently pass span validation.

### Current Conclusion

GLiNER currently provides the highest overall PII detection performance,
with an F1-score of **0.915**.

It also achieves the highest performance on both structured-style inputs
(F1 = **0.877**) and free-text inputs (F1 = **0.965**).

spaCy is the fastest and most memory-efficient detector in the current
benchmark, but provides substantially lower detection quality, particularly
on structured-style inputs.

Hugging Face provides an intermediate trade-off between detection quality
and computational cost.


### Performance Results

The performance benchmark currently uses 36 synthetic text examples.

Each detector is evaluated in a separate Python process so that memory
measurements are not affected by previously loaded models.

| Detector     | Loading Time (s) | Inference / Example (s) | Memory After Loading (MB) | Memory After Inference (MB) |
| ------------ | ---------------: | ----------------------: | -------------------------: | --------------------------: |
| spaCy        |           2.3982 |                  0.006942 |                     329.36 |                     330.72 |
| Hugging Face |           4.8767 |                  0.024776 |                     396.61 |                    1045.12 |
| GLiNER       |           5.0755 |                  0.057249 |                     418.42 |                    1231.18 |


| Detector     | Precision | Recall | F1 |
| ------------ | --------: | -----: | --: |
| spaCy        |     0.461 |  0.722 | 0.562 |
| Hugging Face |     0.826 |  0.732 | 0.776 |
| GLiNER       |     0.892 |  0.938 | **0.915** |

spaCy is currently the fastest and most lightweight approach in the benchmark.

GLiNER provides the highest detection quality but has the highest measured
inference time and memory usage.

Hugging Face provides an intermediate trade-off between detection quality and
computational cost.

The memory values represent process-level resident memory measurements and
should not be interpreted as the exact model size.



### Ground-Truth Validation

The ground-truth dataset uses character-level entity spans with explicit
`start` and `end` offsets.

All current ground-truth entities were validated by checking that the annotated
span corresponds exactly to the annotated entity value.

```text
Total entities: 97
Valid entities: 97
Invalid entities: 0
The ground-truth generation was also updated to handle repeated entity values
using whole-word matching and explicit occurrence selection where necessary


