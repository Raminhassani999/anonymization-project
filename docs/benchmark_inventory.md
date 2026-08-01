# Benchmark Inventory

## Objective

The objective of the benchmark is to compare different approaches for detecting and anonymizing Personally Identifiable Information (PII) in healthcare datasets.

---

## Baseline Method

### Rule-Based Detection

Technique:

* Regular Expressions (Regex)

Current capabilities:

* Email detection
* Phone number detection
* Date detection
* Patient Code detection
* Italian Tax Code detection

Status:

Completed.

---

## Planned AI-Based Methods

### Named Entity Recognition (NER)

Purpose:

Detect entities that cannot be reliably identified using regular expressions.

Examples:

* First Name
* Surname
* Person names
* Organizations
* Locations

Status:

Planned.

---

### Transformer-Based Models

Purpose:

Evaluate pretrained language models specialized for PII detection.

Status:

Planned.

---

### Local Small Language Models (SLMs)

Purpose:

Evaluate locally executed language models for privacy-preserving anonymization.

Status:

Planned.

---

## Evaluation Criteria

The following aspects will be compared:

* Detection accuracy
* Precision
* Recall
* F1-score
* Execution time
* Ease of implementation
* Scalability
* Suitability for healthcare datasets

---

## Current Progress

| Method                | Status      |
| --------------------- | ----------- |
| Regex                 | Completed   |
| Rule-Based Baseline   | In Progress |
| NER                   | Planned     |
| Transformer Models    | Planned     |
| Local SLM             | Planned     |
| Performance Benchmark | Planned     |
