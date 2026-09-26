# Phase 2 Wiki Schema

## 1. Purpose

This schema defines the structure and operating rules of the LLM-maintained knowledge wiki.

The wiki is generated and maintained by local language models served through Ollama.

The wiki must remain grounded in the anonymized source material and must never introduce personal identifiable information.

---

## 2. Wiki Structure

The wiki uses the following structure:

phase2/
├── sources/
│   └── <immutable raw sources>
├── wiki/
│   ├── index.md
│   ├── log.md
│   ├── overview.md
│   ├── conventions.md
│   ├── glossary.md
│   ├── sources/
│   ├── entities/
│   ├── concepts/
│   └── analyses/
└── schema.md

### Page categories

- Source pages: summaries of individual source documents.
- Entity pages: specific identifiable objects or actors that can have a stable identity in the knowledge base.
- Concept pages: general domain ideas, conditions, methods, processes, properties, definitions, or other abstractions.
- Analysis pages: comparisons, syntheses, and useful answers that are intentionally filed into the wiki.

### Entity and Concept Classification Rules

Use the following distinction consistently.

#### Entity

An entity is a specific identifiable object, actor, artifact, organization, cohort, tool, or other item that can have a stable identity and its own page.

Typical entity examples:

- Person
- Organization
- Cohort
- Dataset
- Tool
- Software system
- Artifact
- Named object

Do not classify a general disease, condition, method, process, property, or abstract idea as an entity.

#### Concept

A concept is a general domain idea or abstraction.

Typical concept examples:

- Disease
- Medical condition
- Method
- Procedure
- Theory
- Process
- Property
- Definition
- Measurement concept
- Domain principle

Concepts may have their own concept pages when they are important enough to be reused or referenced by other wiki pages.

#### Classification Rules

1. Classify each candidate according to its meaning, not merely according to how it is written.
2. A named or specific object with a stable identity is an entity.
3. A general domain idea, condition, process, property, or method is a concept.
4. Do not classify the same item as both an entity and a concept unless the source clearly uses the item in two different meanings.
5. Do not create an entity or concept merely because the model can infer one.
6. Extract only items explicitly supported by the source.
7. Do not add synonyms or paraphrases as separate items.
8. Normalize repeated mentions of the same item to one canonical name.
9. Preserve the canonical wording used by the source whenever practical.
10. If classification is genuinely ambiguous, do not guess. Record the item under the category best supported by the source and mark the uncertainty.

For the smoke-test source, diseases and domain ideas such as "Diabetes", "Type 2 diabetes", and "Insulin resistance" are concepts, not entities.
## 3. Source Rules

- Source files are immutable and read-only.
- Source files come from the anonymized Phase 1 output or documented synthetic sources.
- Never modify source files during ingest.
- Never use real personal data.
- All generated knowledge must remain grounded in the available source material.

---

## 4. Source Page Template

Each source page must use this structure:

# <Source Title>

## Summary

A concise summary of the source.

## Key Facts

Important factual statements supported by the source.

## Entities

Important entities identified in the source.

## Concepts

Important concepts identified in the source.

## Claims

Important claims that may be referenced by other pages.

## Source Reference

A reference to the original immutable source file.

---

## 5. Entity Page Template

# <Entity Name>

## Summary

Short description of the entity.

## Evidence

Facts about the entity supported by source pages.

## Related Concepts

Links to related concept pages.

## Related Sources

Links to source pages containing evidence about the entity.

## Uncertainty

State uncertainty explicitly when evidence is incomplete or conflicting.

## Contradictions

Record conflicting claims instead of silently choosing one.

---

## 6. Concept Page Template

# <Concept Name>

## Definition

Definition supported by the sources.

## Key Facts

Important supported facts.

## Related Entities

Links to relevant entity pages.

## Related Concepts

Links to related concept pages.

## Sources

Citations to the source pages supporting the content.

## Uncertainty

State uncertainty when applicable.

## Contradictions

Record conflicting claims and link to the supporting sources.

---

## 7. Analysis Page Template

# <Analysis Title>

## Question

The question or analytical purpose.

## Answer

The synthesized answer.

## Evidence

The source and wiki evidence used to produce the answer.

## Limitations

Important uncertainties or missing evidence.

## Citations

Citations to the relevant wiki pages and source pages.

---

## 8. Naming Conventions

- Use lowercase filenames.
- Use descriptive names.
- Use hyphens between words.
- Keep filenames stable once a page exists.
- Do not create a new page when an existing page represents the same entity or concept.

Examples:

- `type-2-diabetes.md`
- `insulin-resistance.md`
- `source-diabetology-overview.md`

---

## 9. Linking Conventions

- Use relative Markdown links.
- Link existing pages instead of duplicating information.
- Add cross-references when two pages are meaningfully related.
- Do not create links to pages that do not exist.
- Prefer linking to canonical pages rather than creating near-duplicates.

Example:

[Insulin Resistance](../concepts/insulin-resistance.md)

---

## 10. Citation Conventions

Every non-trivial factual claim should be traceable to a source.

Use a provenance chain:

claim
→ wiki page
→ source page
→ immutable source document

Citations should identify the source page and, when possible, the relevant source section.

Do not present unsupported model-generated information as fact.

---

## 11. Uncertainty

When evidence is incomplete, ambiguous, or weak:

- explicitly state the uncertainty;
- do not invent missing information;
- preserve the supported part of the claim;
- link to the relevant evidence.

---

## 12. Contradictions

When sources disagree:

- do not silently overwrite one claim with another;
- preserve both claims;
- identify the conflicting sources;
- explicitly mark the contradiction;
- do not resolve the contradiction unless the available evidence supports a resolution.

---

## 13. Index Rules

`wiki/index.md` is a content-oriented catalog.

It must:

- contain a one-line summary for every wiki page;
- group pages by category;
- help the model identify which existing pages may be affected by a new source;
- avoid becoming a simple filesystem listing.

---

## 14. Log Rules

`wiki/log.md` is append-only.

It records every:

- ingest operation;
- query operation;
- lint operation.

Each entry must record:

- date/time;
- operation;
- source or question;
- model;
- quantization;
- relevant parameters;
- prompt/schema version;
- timing;
- files changed.

Example:

## [2026-09-21] ingest | smoke_source

- model: llama3.2:3b
- quantization: Q4_K_M
- prompt_version: schema-v1
- files_changed:
  - sources/smoke_source.md
  - wiki/sources/smoke-source.md
  - wiki/index.md
  - wiki/log.md

---

## 15. Ingest Procedure

For every ingest operation, follow exactly this order:

1. Read the source.
2. Read `schema.md`.
3. Read `wiki/index.md`.
4. Identify affected existing pages.
5. Update existing pages before creating new pages.
6. Create new pages only when necessary.
7. Add required cross-references.
8. Update `wiki/index.md`.
9. Append the operation to `wiki/log.md`.
10. Validate the generated wiki.
11. Run the privacy regression check.
12. Record the resulting file diff.

The same source must not create duplicate content when ingested twice.

---

## 16. Query Procedure

For every query:

1. Read `schema.md`.
2. Read the relevant wiki pages.
3. Answer using only supported wiki evidence.
4. Provide citations to the supporting wiki and source pages.
5. State when the wiki does not contain enough evidence.
6. Do not invent unsupported information.
7. Record the query in `wiki/log.md`.

A query answer may optionally be filed as an analysis page.

---

## 17. Lint Procedure

Lint checks the wiki for:

- contradictions;
- stale claims;
- orphan pages;
- broken links;
- missing cross-references;
- incomplete index entries;
- schema violations;
- citation problems.

Lint results must be recorded in `wiki/log.md`.

---

## 18. Idempotence

Ingesting the same source twice must not create duplicate pages or duplicate content.

The resulting wiki should remain logically unchanged by repeated ingestion of an already processed source.

---

## 19. Schema Version

Current schema version:

`schema-v1`

Every operation log entry must record the schema/prompt version used.

Changes to this schema are experiments and must be versioned and evaluated separately.