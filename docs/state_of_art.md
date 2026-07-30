# State of the Art: Data Anonymization and PII Detection

## 1. Introduction

The increasing use of data-driven approaches in healthcare and research requires the analysis of large amounts of information. Medical datasets can provide valuable insights, but they often contain sensitive information related to individuals.

To protect privacy, personal information must be identified and anonymized before the data can be used for analysis or shared with other parties.

This project focuses on the study and implementation of techniques for detecting Personally Identifiable Information (PII) and preparing heterogeneous datasets for anonymization.

## 2. Data Anonymization

Data anonymization is the process of transforming data so that individuals cannot be identified from the information contained in the dataset.

The main goal of anonymization is to preserve the usefulness of data for analysis while protecting the privacy of the people represented in the dataset.

This is particularly important in healthcare datasets because medical information can contain sensitive details about patients, including identity information, demographic information, and clinical records.

Different anonymization techniques exist depending on the type of data and the level of privacy required.

## 3. Types of transformations used during Anonymization

A - Redaction : completely remove the value : Elena Verdi ===> REDACTED
thus it is irreversible , safest but loses information
B - Generalization : Reduce precision while preserving usefulness ===> 1998 / 04 / 12 is our data we can write it as 1998 / 04 
useful for Statistics , Age Analysis , Reporting 
C - Masking : Hide only part of the value : Elena@gmail.com ===> Exxx@gmail.com
D - Pseudonymization : Replacing the value with a stable identifier : Elena Verdi ===> Person_001


## 4. Personally Identifiable Information (PII)

Personally Identifiable Information (PII) refers to any information that can directly identify an individual or can be combined with other information to identify a specific person.

In the context of healthcare datasets, PII is particularly important because medical records often contain both personal identifiers and sensitive clinical information. Before using these datasets for research or analysis, identifying and protecting PII is necessary to preserve patient privacy.

### 4.1 Direct Identifiers

Direct identifiers are information that can immediately identify an individual.

Examples include:

- Full name
- Tax code
- Patient identification code
- Phone number
- Email address
- Home address

In the diabetology dataset used in this project, examples of possible direct identifiers include:

First Name
Surname
Tax Code
Patient Code


These fields require strong protection because they directly link the data to a specific person.

---

### 4.2 Quasi-identifiers

Quasi-identifiers are attributes that may not identify a person individually but can become identifying when combined with other information.

Examples:

- Date of birth
- Age
- Gender
- Location
- Dates of medical visits

For example:

Birth Date + Gender + Location

may identify a person even if the name is removed.

In the diabetology dataset, examples include:
Birth Date
Sex
Age At Assessment
Assessment Date


These attributes may require transformations such as generalization or removal depending on the anonymization objective.

---

### 4.3 Sensitive Attributes

Sensitive attributes are information that describes personal conditions and should be protected even when direct identifiers are removed.

Examples:

- Medical diagnosis
- Laboratory results
- Treatment information
- Clinical history

In this project, examples include:

Diabetes Diagnosis Year
Renal Failure
Blood Glucose
HbA1c
Medication Information


These fields may not identify an individual by themselves, but they represent sensitive health information.

---

### 4.4 PII Detection Approaches

To identify PII automatically, different techniques can be used.

### Rule-based detection

Rule-based methods use predefined patterns to identify sensitive information.

Example:

Regular expressions (Regex) can detect:


Phone numbers
Dates
Tax codes
Email addresses



Advantages:

- Fast
- Explainable
- Easy to customize

Limitations:

- Requires manually created rules
- Cannot understand context


### Machine Learning and NLP-based detection

Named Entity Recognition (NER) models can detect entities based on language context.

Example:

Input: 
Maria Rossi works at Microsoft in Rome.


NER output:

Maria Rossi → PERSON
Microsoft → ORGANIZATION
Rome → LOCATION


Advantages:

- Understands context
- Can detect entities without manually defining every pattern

Limitations:

- Depends on model quality
- Can produce incorrect predictions


## Data Ingestion and Data Normalization

Real-world anonymization systems usually receive data from different sources and file formats. Healthcare datasets, for example, can be stored in structured formats such as Excel, CSV, and JSON files, or in unstructured formats such as plain text documents.

Before applying privacy-preserving techniques, the data must be correctly loaded and prepared. A data ingestion layer is responsible for reading information from different sources and converting it into a format that can be processed by the following stages of the pipeline.

### Data Loaders

Because different file formats have different internal structures, specific loading mechanisms are required for each type of source.

Examples:

- Excel files contain tables organized into rows and columns.
- CSV files represent structured tabular data separated by delimiters.
- JSON files store information using key-value structures.
- TXT files contain unstructured textual information.

A loader is responsible only for reading the data from its original format and returning the extracted information. Keeping separate loaders improves modularity and makes it easier to extend the system with new data sources.

### Data Normalization

After loading the data, different sources may produce different types of objects. For example, structured files can be represented as tabular data, while text files are represented as plain text.

A normalization layer creates a common representation for all input sources. The goal is not to change the content of the data, but to provide a consistent structure that can be used by later components.

A normalized representation can contain:

- Source type: the original format of the data (Excel, CSV, JSON, TXT).
- Data type: whether the information is structured or unstructured.
- Content: the actual loaded data.

This approach allows later stages, such as PII detection and anonymization, to operate independently from the original data format.

### Automatic File Processing

To improve scalability, a universal loading mechanism can automatically identify the input format and select the appropriate loader.

The general workflow is:

Different data sources
↓
Format-specific loader
↓
Normalized representation
↓
PII detection
↓
Anonymization

This modular architecture improves maintainability because each component has a specific responsibility:
- Loaders handle data extraction.
- The normalization layer handles standardization.
- Detection modules analyze sensitive information.
- Anonymization modules apply privacy transformations.


