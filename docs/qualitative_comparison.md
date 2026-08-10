# Qualitative Comparison

## 1. Overview

A qualitative comparison was performed by inspecting detector outputs on the same
synthetic examples used in the quantitative benchmark.

The comparison focuses on:

- correctly detected entities;
- missed PII entities;
- false positives and over-detection;
- entity boundary errors;
- entity type errors;
- behavior on multiple entities within the same text;
- consistency of detected spans.

The three NER-based approaches were compared using the same evaluation dataset and
the same entity categories: `person`, `organization`, `location`, and `date`.

---

## 2. spaCy

spaCy showed the largest number of qualitative detection problems among the three
NER approaches.

### 2.1 False positives and over-detection

spaCy frequently detected text that was not itself a PII entity or assigned an
entity to an overly broad span.

For example:

```text
Original:
Luigi Bianchi works for Microsoft.

spaCy prediction:
"Luigi Bianchi works for Microsoft" → person


Instead of identifying the person name only, the prediction covers the entire
sentence.

Another example is:

Original:
Giulia Ferraro lives in Milan.

spaCy prediction:
"Giulia" → location
"Milan" → organization

Both the entity boundaries and entity types are incorrect.

spaCy also produced predictions such as:

"Rome on 12/05/2023" → misc
"March 1985" → date
"Rome | Birth Date" → misc
showing that structured text containing labels and separators can cause the
detector to expand an entity beyond its intended span.

2.2 Boundary errors

spaCy sometimes detected the correct general concept but included surrounding
words.

For example:
Expected:
University of Messina → organization

Predicted:
the University of Messina → organization
The entity type is correct, but the span contains the preceding article.

Another example is:
Expected:
15 March 2024 → date

Predicted:
2024 → date

Only part of the date was detected.

2.3 Type errors

spaCy also confused entity categories.

For example:
Policlinico di Messina
Expected: organization
Predicted: person

Giulia Ferraro
Expected: person
Predicted: organization


Similar organization/location confusions occurred for entities such as
Messina, Milan, and University of Messina.

2.4 Missed entities

spaCy also missed several expected locations.

For example:
Francesca Romano lavora a Roma.

Expected:
Francesca Romano → person
Roma → location

Missed:
Roma → location

The detector therefore recognized part of the PII in the sentence but failed to
detect the location entity.

2.5 Overall qualitative observation

spaCy performs reasonably well on simpler free-text entities but is more
sensitive to structured text, entity boundaries, and entity-type ambiguity.

This behavior is consistent with its lower overall precision and F1 score in the
quantitative benchmark.

3. Hugging Face

The Hugging Face detector produced substantially fewer false positives than
spaCy and generally produced cleaner entity spans.

3.1 False positives

Only a small number of false positives were observed.

Examples include:

"na" → location
"clin" → organization
"Messina" → location

These predictions represent short fragments or repeated locations that were not
annotated as entities at those positions.

3.2 Missed entities

The main qualitative weakness was missed dates.

Examples include:
15 March 2024
2024-06-20
12/05/2023
15 marzo 2024

Several date expressions were not detected even though they were present in the
ground truth.

The detector also missed some locations, such as Messina.

3.3 Boundary errors

Hugging Face occasionally detected only part of a longer entity.

For example:
Expected:
Policlinico di Messina → organization

Predicted:
Messina → location

Expected:
Policlinico di Messina → organization

Predicted:
Poli → location

These predictions demonstrate both span truncation and entity-type confusion.

3.4 Type errors

The most consistent type error was confusion between organizations and
locations.

For example:
Policlinico di Messina
Expected: organization
Predicted: location
University of Messina
Expected: organization
Predicted: location

However, compared with spaCy, the number and severity of these errors were
considerably lower.

3.5 Overall qualitative observation

The Hugging Face detector provides a better balance between precision and
recall than spaCy. Its main remaining weaknesses are date detection and
organization/location classification


4. GLiNER

GLiNER produced the strongest qualitative results among the evaluated NER
approaches.

4.1 Boundary and type errors

No boundary errors were reported for GLiNER in the qualitative error analysis.

No type errors were reported either.

This is a significant difference from both spaCy and Hugging Face.

In particular, GLiNER correctly avoided the organization/location and
person/organization type confusions observed in the other detectors.

4.2 False positives

GLiNER still produced several false positives, particularly around structured
labels.

For example:
Patient: Luigi Bianchi | Hospital: Policlinico di Messina | City: Messina

False positives:
"City" → location
"Messina" → location

Similar predictions occurred for labels such as:

City
Country

This suggests that the detector can sometimes interpret field labels themselves
as entities.

4.3 Missed entities

GLiNER missed only a small number of entities in the qualitative analysis.

The main remaining problem was the location Messina.

For example:

Francesca Romano studies at the University of Messina.

Missed:
Messina → location


The same location was missed in some structured examples.

4.4 Overall qualitative observation

GLiNER produced the cleanest entity boundaries and entity types among the
three NER detectors.

Its remaining errors were concentrated mainly around:

locations appearing inside organization names;
structured field labels such as City and Country;
repeated location mentions.

This is substantially narrower than the error patterns observed for spaCy and
Hugging Face.

5. Side-by-Side Comparison

| Aspect                       | spaCy       | Hugging Face                    | GLiNER                |
| ---------------------------- | ----------- | ------------------------------- | --------------------- |
| False positives              | High        | Low                             | Low                   |
| Boundary errors              | Frequent    | Occasional                      | None observed         |
| Type errors                  | Frequent    | Occasional                      | None observed         |
| Missed entities              | Several     | Mainly dates and some locations | Few, mainly locations |
| Structured text              | Weak        | Better                          | Strongest             |
| Entity span quality          | Weak        | Moderate                        | Strongest             |
| Overall qualitative behavior | Error-prone | Balanced                        | Most consistent       |


Example: Multiple Entities
A useful example is: Francesca Romano lavora a Roma.
The expected entities are: 
Francesca Romano → person
Roma → location

spaCy produced multiple conflicting predictions for this example, including an
incorrect organization classification for Francesca Romano and a duplicated
location prediction for Roma. It also missed the correctly positioned
location in the false-negative analysis.

This illustrates how overlapping or conflicting predictions can complicate the
downstream anonymization layer.


7. Example: Organization vs Location

Another important example is: Mario Rossi visited Policlinico di Messina.
The expected organization is: Policlinico di Messina → organization

spaCy classified the hospital as a person, while Hugging Face classified it as
a location.

These errors matter for anonymization because the detector may still identify
the sensitive span but assign the wrong anonymization category.

GLiNER did not produce a type error for this example

8. Example: Dates

Dates exposed another difference between the approaches.

For example: Mario Rossi was admitted on 15 March 2024.

Hugging Face missed the complete date expression.

spaCy also showed partial-date behavior in several examples, detecting values
such as: 2024 instead of the complete: 15 March 2024 This demonstrates that date detection is not only a question of recognizing a
date token, but also of correctly identifying the complete entity span.

9. Implications for Anonymization

The qualitative results demonstrate why detector quality cannot be evaluated
only by counting detected entities.

A detector can identify a sensitive region while still producing an incorrect
result because:

the entity type is incorrect;
the entity span is too short;
the entity span is too long;
unrelated surrounding text is included;
a repeated entity is detected inconsistently;
a non-PII label is incorrectly treated as PII.

These errors directly affect the anonymization output.

For example, a prediction such as : "Luigi Bianchi works for Microsoft" → person 
could cause the anonymization layer to replace substantially more text than
intended.

Similarly, detecting only: 2024 instead of: 15 March 2024 
can leave part of a sensitive date visible.

Therefore, span accuracy and entity-type accuracy are important for reliable
end-to-end anonymization.



10. Overall Qualitative Findings

The qualitative inspection supports the quantitative benchmark.

spaCy

spaCy showed the broadest range of error types, particularly false positives,
boundary errors, and entity-type errors. Its behavior was less reliable on
structured text containing labels, separators, and multiple entities.

Hugging Face

The Hugging Face detector substantially reduced false positives compared with
spaCy. Its main weaknesses were missed dates and organization/location
confusion.

GLiNER

GLiNER produced the cleanest entity boundaries and entity types. No boundary
or type errors were observed in the qualitative error analysis. Its remaining
errors were mainly false positives involving structured labels and missed
location mentions.

Overall, the qualitative analysis agrees with the quantitative results:
GLiNER provides the most consistent detection behavior on the evaluation
dataset, while spaCy shows the largest number of qualitative failure modes.