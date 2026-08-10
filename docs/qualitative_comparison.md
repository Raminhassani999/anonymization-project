# Qualitative Comparison

## Overview

The approaches were evaluated on the same synthetic inputs containing structured PII and free-text PII.

The comparison focused on missed entities, over-detection, formatting artifacts, span boundaries, and consistency of anonymization.

## Structured Data

The rule-based anonymizer performs deterministic transformations according to the field policy.

Examples include:

* Patient Code → stable pseudonym
* First Name → masked value
* Surname → masked value
* Tax Code → partial masking
* Birth Date → year-level generalization
* Assessment Date → year-level generalization
* Age At Assessment → decade range

This provides predictable output and preserves the structure of the dataset.

## Free Text

The free-text anonymizer replaces detected entities with type-specific placeholders:

* person → `[PERSON]`
* organization → `[ORGANIZATION]`
* location → `[LOCATION]`
* date → `[DATE]`
* misc → `[MISC]`

Entities are replaced from right to left so that replacing one span does not invalidate the character offsets of entities appearing earlier in the text.

## Detector Differences

### spaCy

spaCy produced the lowest F1 score among the evaluated model-based detectors. It was also the fastest approach.

Its main weakness in this benchmark was incomplete detection of PII in structured fields and lower overall recall.

### Hugging Face

The Hugging Face detector substantially improved precision compared with spaCy and achieved a stronger balance between precision and recall.

It required more memory and inference time than spaCy.

### GLiNER

GLiNER produced the strongest overall detection results.

It achieved high recall on both structured and free-text examples and produced the highest end-to-end exact-output match rate.

## Recurring Failure Patterns

The evaluation indicates that:

1. Structured identifiers are better handled by deterministic rules than by general-purpose NER alone.
2. Free-text PII benefits substantially from contextual NER models.
3. False positives can occur when model predictions are applied indiscriminately to structured columns.
4. Exact output matching is stricter than entity-level recall because a single incorrect span or replacement can make the complete output differ from the reference.
5. Stable pseudonymization is useful when the same identifier appears repeatedly because it preserves linkage between records.

## Summary

The qualitative comparison supports a hybrid architecture: deterministic rules for highly structured identifiers and model-based NER for contextual free-text PII.
