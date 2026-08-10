# Progress Report

## Project Overview

The objective of this project is to develop a modular anonymization framework capable of processing healthcare datasets, detecting Personally Identifiable Information (PII), and anonymizing sensitive data using both rule-based and AI-based approaches. The current implementation focuses on building the data loading pipeline and the rule-based PII detection baseline.

---

# Phase 1 – Project Analysis and Research

### Completed

* Studied the project objectives and anonymization workflow.
* Reviewed healthcare data anonymization concepts.
* Documented the State of the Art.
* Researched different anonymization techniques including:

  * Redaction
  * Masking
  * Generalization
  * Pseudonymization
* Introduced rule-based detection using Regular Expressions (Regex) as the baseline approach.

---

# Phase 2 – Data Loading and Normalization

## Individual File Loaders

Implemented dedicated loaders for multiple file formats:

* CSV Loader
* Excel Loader
* JSON Loader
* TXT Loader

Each loader is responsible for reading its specific file format and returning its content.

---

## Common Data Format

Implemented a common intermediate representation using `create_common_format()`.

Every loaded file is converted into the following structure:

```python
{
    "source": "...",
    "type": "...",
    "content": ...
}
```

This standardizes the input regardless of the original file format and allows all subsequent modules to process data uniformly.

---

## Universal Loader

Implemented `universal_loader.py`.

The universal loader automatically determines the file type from its extension and calls the appropriate loader.

Supported formats:

* CSV
* Excel (.xlsx)
* JSON
* TXT

This removed the need to manually select a loader for each file type.

---

## Dataset Validation

Successfully tested the universal loader using the synthetic diabetology dataset.

Verified:

* Dataset loading
* Dataset preview
* Dataset dimensions
* Column names

---

# Phase 3 – Rule-Based PII Detection

## Initial Regex Detector

Developed the first version of the regex detector capable of identifying common PII patterns.

Initially implemented detection for:

* Email addresses
* Phone numbers
* Dates

---

## Healthcare-Specific Detection

Extended the detector with patterns specific to the medical dataset.

Added support for:

* Patient Codes
* Italian Tax Codes (Codice Fiscale)

These identifiers are important structured PII attributes commonly found in healthcare records.

---

## Modular Refactoring

Refactored the detector into reusable components.

Created dedicated detection functions:

* `detect_email()`
* `detect_phone()`
* `detect_date()`
* `detect_patient_code()`
* `detect_tax_code()`

This eliminated duplicated regex logic and improved maintainability.

---

## Generic Text Detection

Implemented `detect_pii(text)`.

This function combines all specialized detectors and can be used for unstructured text sources such as:

* TXT documents
* OCR output
* PDF extracted text

---

## Structured Dataset Detection

Implemented `detect_dataframe(df)`.

This function scans structured datasets row by row and records:

* Row index
* Column name
* Original value
* Detected PII

The output is returned as a structured detection report.

---

## Column-Aware Detection

Introduced a column mapping mechanism using `PII_COLUMNS`.

Example:

```python
PII_COLUMNS = {
    "Patient Code": "patient_code",
    "Tax Code": "tax_code",
    "Birth Date": "date",
    "Assessment Date": "date"
}
```

Instead of applying every regex to every dataset column, the detector now routes each relevant column to the appropriate detection function.

Benefits:

* Improved efficiency
* Cleaner architecture
* Easier maintenance
* Better scalability
* Simpler integration with future AI models

---

# Current Project Pipeline

```
Input File
      │
      ▼
Universal Loader
      │
      ▼
Common Format
      │
      ▼
Column-Aware Regex Detection
      │
      ▼
Structured Detection Report
```

---

# Current Status

## Completed

* Project research
* State of the Art documentation
* File loaders
* Universal Loader
* Common data representation
* Synthetic dataset validation
* Rule-based regex detector
* Healthcare-specific regex patterns
* Modular detector architecture
* Column-aware detection pipeline

---

## Next Objectives

The next development phase will focus on implementing the anonymization module.

Planned tasks include:

* Rule-based redaction
* Data masking
* Pseudonymization
* Generalization

After completing the rule-based anonymization baseline, the project will continue with:

* Named Entity Recognition (NER)
* Transformer-based PII detection
* Local Small Language Models (SLMs)
* Performance comparison between rule-based and AI-based approaches


## Progress Update (Today's Work)

### Rule-Based Anonymization Improvements
- Implemented a **generalization** anonymization strategy.
- Added support for generalizing:
  - Birth Date → Year of birth
  - Assessment Date → Assessment year
  - Age At Assessment → Age ranges (e.g., 70–79)

### Policy-Based Anonymization
- Refactored the anonymization engine to use a configurable anonymization policy.
- Removed the global anonymization method parameter.
- Introduced an `ANONYMIZATION_POLICY` dictionary that assigns a different anonymization strategy to each PII column.

Current policy:
- Patient Code → Pseudonymization
- Tax Code → Masking
- Birth Date → Generalization
- Assessment Date → Generalization
- Age At Assessment → Generalization

### Refactoring
- Simplified `main.py` by removing the anonymization method argument.
- Updated `anonymize_dataframe()` to automatically select the anonymization strategy based on the configured policy.
- Improved modularity and maintainability of the anonymization pipeline.

### Testing
- Successfully tested the complete anonymization workflow on the diabetology synthetic dataset.
- Verified that:
  - Patient codes are consistently pseudonymized.
  - Tax codes are correctly masked.
  - Dates are generalized to years.
  - Ages are generalized into decade intervals.


  ## AI-Based PII Detection and Benchmarking

### Completed

- Added Hugging Face NER as a second AI-based PII detection approach.
- Added GLiNER as a third AI-based PII detection approach.
- Created a common `Detector` interface so spaCy, Hugging Face, and GLiNER can be evaluated through the same pipeline.
- Created a ground-truth evaluation dataset containing English and Italian examples covering persons, locations, organizations, and dates.
- Implemented TP, FP, FN, Precision, Recall, and F1-score evaluation.
- Extended the ground truth to use character-level entity spans (`start` / `end`).
- Updated the detectors to return their predicted entity spans.
- Implemented span-based evaluation comparing predicted entities with the ground truth.

### Current Benchmark Results

| Detector | Precision | Recall | F1 |
|---|---:|---:|---:|
| spaCy | 0.661 | 0.860 | 0.747 |
| Hugging Face | 0.897 | 0.814 | 0.854 |
| GLiNER | 0.976 | 0.953 | **0.965** |

GLiNER currently achieves the best overall detection performance on the evaluation dataset.

### Next Steps

- Benchmark inference/runtime performance.
- Measure model loading time.
- Measure memory/resource usage.
- Perform detailed false-positive and false-negative analysis.
- Expand the evaluation dataset with more representative examples.
- Determine the most suitable detector or hybrid detection strategy.



### Performance Benchmark

A performance benchmark was implemented to compare model loading time,
steady-state inference time, and process memory usage on the same hardware.

The current benchmark contains 18 synthetic text examples and measures each
detector in a separate Python process to avoid memory contamination between
models.

| Detector | Loading Time (s) | Avg. Inference / Example (s) | Memory After Loading (MB) | Memory After Inference (MB) |
|---|---:|---:|---:|---:|
| spaCy | 2.4785 | 0.006019 | 328.70 | 329.91 |
| Hugging Face | 4.8681 | 0.022047 | 395.72 | 1042.75 |
| GLiNER | 4.9420 | 0.056757 | 417.74 | 1223.95 |

spaCy is currently the fastest and has the lowest measured memory footprint.
GLiNER provides the highest detection quality but has the highest inference
time and memory usage. Hugging Face provides an intermediate trade-off.

### Error Analysis

An error-analysis script was implemented to distinguish between:

- False positives
- False negatives
- Boundary errors
- Entity-type errors

The current analysis shows that spaCy produces more false positives, incorrect
entity types, and overly broad spans. Hugging Face has relatively high
precision but misses several entities, particularly dates, and produces some
partial entity spans. GLiNER produces substantially fewer errors, with the
remaining errors concentrated mainly around specific location entities.

### Ground-Truth Validation

The ground-truth annotations were validated using their character-level
`start` and `end` positions.

- Total annotated entities: 43
- Valid entity spans: 43
- Invalid entity spans: 0

Therefore, all current ground-truth character spans are internally consistent.

### Current Findings

GLiNER currently provides the strongest detection performance on the evaluation
dataset, with an F1-score of 0.965. spaCy provides substantially lower
computational cost, while Hugging Face provides an intermediate trade-off.

The current results should be considered an initial benchmark because the
evaluation dataset is still relatively small and additional benchmark
dimensions remain to be evaluated.

### Next Steps

- Expand the synthetic evaluation dataset.
- Separate quantitative results for structured fields and free-text documents.
- Measure throughput in records/second.
- Further investigate peak memory and model size on disk.
- Evaluate consistency/determinism across repeated runs.
- Perform qualitative comparison of the actual anonymized outputs.
- Evaluate context adaptability of each approach.
- Develop a final comparison matrix and recommendation.