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




## Current Rule-Based Baseline

The current baseline anonymization system consists of:

### Detection
- Regular-expression based PII detection
- Column-aware detection for structured medical datasets

### Supported PII Types
- Patient Code
- Tax Code
- Birth Date
- Assessment Date
- Age At Assessment

### Supported Anonymization Techniques
- Redaction
- Masking
- Pseudonymization
- Generalization

### Configuration

The anonymization engine uses a configurable policy that assigns a different anonymization strategy to each sensitive attribute.

This implementation serves as the baseline system that will later be compared with AI-based Named Entity Recognition (NER) approaches.


Benchmark Progress Update

The PII detection benchmark has been expanded to compare three AI-based approaches: spaCy, Hugging Face NER, and GLiNER. A common detector interface was introduced so that the different models can be evaluated using the same pipeline.

A ground-truth dataset was created and extended to include English and Italian examples, names, locations, organizations, and dates. The evaluation was then implemented using TP, FP, FN, Precision, Recall, and F1-score.

The evaluation was further improved by introducing entity spans (start / end positions) in both the ground truth and model predictions. This allows the benchmark to evaluate not only whether an entity was detected, but also whether the correct portion of the text was identified.

Current results on the evaluation dataset are:

Detector	Precision	Recall	F1
spaCy	0.661	0.860	0.747
Hugging Face	0.897	0.814	0.854
GLiNER	0.976	0.953	0.965

Based on the current dataset, GLiNER achieves the best overall detection performance, followed by Hugging Face and spaCy.

Remaining benchmark tasks
Runtime and inference-time comparison
Model loading time
Memory/resource usage
Detailed false-positive and false-negative analysis
Evaluation on a larger and more representative dataset
Final selection of the most suitable detector or hybrid approach

Current status: AI-based PII detection and accuracy benchmarking are complete at an initial level. Performance/resource benchmarking and detailed error analysis are the next steps.