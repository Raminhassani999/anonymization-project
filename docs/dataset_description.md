# Dataset Description

## Dataset

The project currently uses a synthetic diabetology dataset provided in Excel (.xlsx) format.

Dataset file:

```text
data/diabetology/diabetology-synthetic-dataset.xlsx
```

## Dataset Characteristics

* Format: Microsoft Excel (.xlsx)
* Domain: Healthcare / Diabetology
* Number of records: 1,337
* Number of columns: 103

## Data Content

The dataset contains demographic, clinical, laboratory, and treatment information for synthetic patients.

Examples of attributes include:

* Patient Code
* First Name
* Surname
* Birth Date
* Tax Code
* Assessment Date
* Sex
* Height
* Weight
* Blood Pressure
* Laboratory values
* Medication and treatment information

## Personally Identifiable Information (PII)

The current implementation focuses on detecting the following PII fields:

* Patient Code
* Tax Code (Italian Codice Fiscale)
* Birth Date

Future versions will extend detection to:

* First Name
* Surname
* Email Address
* Phone Number
* Other entities detected using Named Entity Recognition (NER).

## Purpose

The dataset is used to develop and evaluate rule-based and AI-based anonymization techniques while preserving the clinical information required for downstream analysis.



## Dataset Processing

The diabetology synthetic dataset is currently used to develop and evaluate the rule-based anonymization pipeline.

The following sensitive attributes are currently processed:

- Patient Code
- Tax Code
- Birth Date
- Assessment Date
- Age At Assessment

The implemented anonymization policy is:

| Attribute | Technique |
|-----------|-----------|
| Patient Code | Pseudonymization |
| Tax Code | Masking |
| Birth Date | Generalization |
| Assessment Date | Generalization |
| Age At Assessment | Generalization |

The anonymized dataset preserves analytical usefulness while reducing disclosure risk by applying different anonymization techniques according to the sensitivity of each attribute.