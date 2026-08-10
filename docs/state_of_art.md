# Practical PII Detection and Anonymization

## 1. Overview

Practical PII anonymization systems generally combine detection with a separate anonymization step. Common detection strategies include deterministic rules and regular expressions, Named Entity Recognition (NER), and transformer-based token-classification models.

For heterogeneous datasets, a useful architecture separates input normalization, PII detection, and anonymization. This allows the same anonymization policies to be applied to structured fields and free-text documents.

## 2. Approaches

| Approach           | Type                                | Structured Data | Free Text | Context Awareness | Deployment       |
| ------------------ | ----------------------------------- | --------------: | --------: | ----------------- | ---------------- |
| Regex / rules      | Deterministic rules                 |          Strong |   Limited | Low               | Very lightweight |
| spaCy NER          | Statistical / NER                   |        Moderate |    Strong | Moderate          | Lightweight      |
| Hugging Face NER   | Transformer token classification    |        Moderate |    Strong | High              | Medium           |
| GLiNER             | Generalist NER / span detection     |        Moderate |    Strong | High              | Medium           |
| Microsoft Presidio | Detection + anonymization framework |          Strong |    Strong | Configurable      | Medium           |

### Regex and rule-based detection

Regular expressions are effective for highly structured identifiers such as dates, tax codes, patient identifiers, email addresses, and phone numbers. They are deterministic, fast, and easy to reproduce, but they have limited contextual understanding and can produce false positives when patterns occur in non-PII values.

The project therefore uses a deterministic rule-based layer as its baseline.

### spaCy NER

spaCy provides production-oriented NLP pipelines and Named Entity Recognition. NER models identify entities such as people, organizations, and locations from textual context.

spaCy is attractive when low latency and a relatively small deployment footprint are important. Its main limitation for this project is that general-purpose NER is not specifically optimized for every type of sensitive identifier.

### Hugging Face token classification

Transformer-based token classification models assign labels to tokens and are commonly used for NER. The Hugging Face Transformers ecosystem supports a wide range of transformer architectures and pretrained token-classification models.

These models can provide stronger contextual detection than simple rules, at the cost of higher model-loading time and memory consumption.

### GLiNER

GLiNER is a generalist entity-recognition approach that can detect entity types specified at inference time. This makes it particularly interesting for PII detection because the desired entity categories can be adapted to the application.

In this project, GLiNER produced the strongest detection and end-to-end anonymization results among the evaluated model-based approaches.

### Microsoft Presidio

Microsoft Presidio provides a dedicated PII detection and anonymization architecture. Its Analyzer combines recognizers including regular expressions, deny lists, rule-based logic, NER models, and contextual information. Its Anonymizer supports operations such as redaction, replacement, hashing, and encryption.

Presidio therefore represents a practical framework-oriented alternative to building the detection and anonymization layers independently.

## 3. Comparison

The approaches represent different points in the quality-versus-complexity trade-off:

* **Regex/rules:** best for deterministic structured identifiers and low latency.
* **spaCy:** useful when lightweight contextual NER is required.
* **Hugging Face transformers:** useful when stronger contextual detection justifies additional resource usage.
* **GLiNER:** useful when flexible entity categories and high detection quality are priorities.
* **Presidio:** useful when a configurable end-to-end PII detection and anonymization framework is preferred.

## 4. Selection for This Project

The project evaluates regex-based detection together with spaCy, Hugging Face, and GLiNER detectors on a shared synthetic benchmark. The final recommendation is therefore based on measured results rather than theoretical capabilities alone.

No real personal data is used in the benchmark.
