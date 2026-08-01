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
