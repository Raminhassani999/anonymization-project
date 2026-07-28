# Building AI-Based Information Systems

### Phase: Automatic and Semi-Automatic Data Anonymization

**Track:** Data Preparation for AI-Based Information Systems

---

## 1. Context

Modern AI-based information systems increasingly ingest data from
heterogeneous, uncontrolled sources — structured tabular files (CSV, XLSX)
and unstructured free-text documents (TXT, notes, reports) — and turn them
into knowledge that is stored, retrieved, and reasoned about by AI
components (retrieval-augmented generation, knowledge synthesis, semantic
search).

Whenever such data may contain personal or sensitive information, it must
be anonymized **before** it is stored or made available to any AI
component. Anonymization sits at a critical junction: it must be effective
enough to prevent re-identification, yet not so aggressive that it destroys
information the rest of the system legitimately needs (e.g. a date, an age
range, a diagnosis category) to produce useful, coherent knowledge
downstream.

This creates two competing pressures that any anonymization solution must
balance:

- **Safety** — sensitive identifiers must not leak into stored data,
  generated knowledge artifacts, or anything an AI model might later
  surface to a user.
- **Utility and context-sensitivity** — over-redaction silently degrades
  the quality of everything built on top of the data. What counts as
  "sensitive" is not universal: the same field (e.g. a date of birth) can
  be critical to preserve in one context (a medical record, where age is
  clinically meaningful) and safely removable in another (a generic
  administrative document).

**The task, in one sentence:** take heterogeneous raw data, normalize it
into a common representation suitable as input to an anonymization
component, run and compare several concrete anonymization approaches, and
produce output that is safe enough to feed into downstream AI components
— while remaining useful for the specific context the data comes from.

This roadmap covers the anonymization step: normalizing heterogeneous
input and evaluating anonymization approaches on it. What gets built on
top of anonymized data — retrieval, knowledge synthesis, downstream AI
reasoning — and how a chosen approach gets integrated into a live system,
are natural next steps to take up afterward.

---

## 2. Expected Outcomes

1. A short, practical **state-of-the-art report** surveying deployable,
   practical anonymization/PII-detection approaches suitable for
   heterogeneous tabular and free-text data.
2. A **common intermediate representation** that converts heterogeneous
   input files (at minimum CSV and TXT; other formats as a stretch goal)
   into a normalized structure that anonymization approaches can consume
   uniformly, regardless of source format.
3. **3–4 working implementations** of anonymization approaches, sharing a
   common, clearly defined interface, evaluated on a shared, representative
   synthetic dataset (no real personal data should ever be used for this
   work).
4. A **qualitative comparison**: side-by-side inspection of output
   differences on the same inputs (what got redacted, what got missed, what
   got over-redacted, formatting artifacts, consistency across repeated
   runs).
5. A **quantitative comparison** across clearly defined metrics (Section
   6), collected via a reproducible benchmark and summarized in
   tables/plots.
6. A **recommendation**: which approach(es) look most promising for which
   contexts, and what a context-aware selection strategy might look like
   (Section 7).
7. A **project repository** maintained throughout the work (Section 3),
   with a README describing, at any point in time, what has been done and
   how to reproduce it.
8. A **containerized deployment** of the resulting solution(s) via Docker
   and Docker Compose, so any approach can be built and run reproducibly
   with a single command.

---

## 3. Onboarding

- A GitHub repository will be provided as the working record of this
  project; use it from the very first exploratory script onward — not just
  as a place to dump a final report at the end.
- Adopt a simple, consistent Git workflow: small, focused commits with
  descriptive messages, one topic per commit rather than large occasional
  dumps, and a `.gitignore` that keeps datasets/model weights/virtual
  environments out of version control.
- Maintain a `README.md` at the root of the repository that is kept up to
  date as work progresses — not written once at the end. It should
  concisely describe: what the project is about, the current state of the
  work, how to set up the environment and reproduce results, and a short,
  dated log of the activities carried out and pushed so far. Treat the
  README as the single entry point a supervisor (or anyone else) can read
  to understand what has been done without needing a separate status
  report.
- Read broadly about how PII detection and anonymization are typically
  approached in practice (rule-based, statistical/NER-based, and
  model-based methods), and about the general architecture of a system
  that ingests heterogeneous data and turns it into knowledge consumed by
  AI components (retrieval, generation, semantic search) — enough to
  understand *why* anonymization quality matters for what comes after,
  without needing to reference any specific existing codebase.
- Set up a local development environment with the libraries needed to
  experiment with PII detection (e.g. a general NLP/NER toolkit, and a
  library for running an open-source language model locally), and confirm
  a minimal end-to-end script (load a file → detect PII → produce output)
  runs before moving on.
- Get comfortable with Docker and Docker Compose, since each anonymization
  approach implemented later should be packaged as a container and
  deployable via Compose (Section 6) — this keeps every approach
  reproducible and easy to run side by side for comparison.

---

## 4. State of the Art

Goal: a **practical**, not purely academic, survey — the emphasis is on
what is actually deployable and self-hostable, and usable inside a real
system. For each candidate approach found, document: what it is,
how it detects/removes PII, licensing, resource requirements (CPU/GPU,
model size), language support, and known limitations.

This survey is the foundation for Section 6: the student is expected to
independently identify and select the specific anonymization approaches
worth implementing and comparing, based on what this research surfaces —
this roadmap intentionally does not prescribe a fixed list. Two examples
to get the exploration started (not a required or exhaustive set):
**OpenAI's Privacy Filter** model (a small, purpose-built token-
classification model for context-aware PII detection), and the use of
**local, self-hosted small language models (SLMs)** prompted to detect
and/or rewrite PII in free text. Beyond these, look broadly — rule/regex
and NER-based toolkits, other purpose-built detection models, and anything
else the research turns up as relevant. All candidates must be
**open-source and free to use** — self-hostable, with no proprietary
licensing or usage fees — since the resulting solutions need to be
runnable and reproducible without depending on a paid third-party
service.

For each candidate covered, write a short summary plus a comparison table
(license, type of model, context-awareness, structured vs. free-text
focus, typical latency class, deployment footprint).

**Outcome:** a written state-of-the-art report, committed to the
repository.

---

## 5. Common Intermediate Format

Design and implement a normalization step that converts heterogeneous
input files into one common shape before anonymization.

- Input formats to support: CSV (including different delimiters/encodings),
  plain TXT (free text, one "document" per record or per file); other
  formats (e.g. spreadsheets, Word/PDF documents) as a stretch goal.
- Output: a common, well-documented structure distinguishing named,
  structured fields (e.g. a set of key/value pairs) from free-text content,
  so every anonymization approach can consume it without format-specific
  branching.
- Handle the structured-vs-free-text distinction explicitly: a structured
  record has named fields (some of which may be linkage/identifier keys
  that must be preserved rather than anonymized, since removing them would
  break the ability to relate records to one another); free text is
  unstructured prose where PII can appear anywhere, in any grammatical
  form.
- Build a **small synthetic test dataset** with realistic-looking but fully
  fake sensitive fields (names, dates of birth, national ID numbers,
  addresses, phone numbers, free-text notes with embedded identifiers) —
  generated with a synthetic-data tool or hand-crafted fake examples,
  **never real personal data**, so the comparison work is safe to run,
  share, and include in the final report.

**Outcome:** a common-format module (or notebook) plus the synthetic
dataset used for all subsequent evaluation, committed to the repository.

---

## 6. Implementing and Comparing Anonymization Approaches

Based on the state-of-the-art research from Section 4, select and
implement 3–4 concrete **automatic, AI-based** anonymization approaches
against the common format from Section 5, behind a shared, simple
interface (e.g. a function or class that takes a record in the common
format and returns an anonymized copy), so they can be run and compared
uniformly. Each approach should be packaged as its own container and
deployable via Docker Compose, so all approaches can be built and run
side by side with a single command.

The choice of which approaches to implement is up to the student, and
should follow directly from what Section 4 finds worth comparing — e.g.
it could include OpenAI's Privacy Filter, one or more local SLMs used as
anonymization judges/rewriters, a purpose-built PII-detection model, or
other AI-based methods surfaced during the research; this roadmap does
not fix the set in advance. At least one of the implemented approaches
should be understood and built at the mechanism level (not just
configured off the shelf), so its behavior can be explained rather than
treated as a black box during the comparison.

In addition, implement a **deterministic, rule-based masking/
pseudonymization baseline** — not counted among the AI-based approaches
above, but used throughout Sections 6.1–6.2 as the fixed reference point
("fast, fully predictable, but context-blind") that every AI-based
approach is compared against.

For each approach (and the baseline): run it over the full synthetic
dataset from Section 5 and keep the raw outputs for the qualitative
comparison below.

### 6.1 Qualitative Comparison

Before any scoring, do a manual, low-level, side-by-side read of the
outputs:

- For a representative sample of records (structured and free-text), lay
  out the original next to each approach's output.
- Note concretely, per record: what was redacted, what should have been
  redacted but wasn't (false negatives), what was redacted but shouldn't
  have been (false positives / over-redaction), and any formatting
  artifacts (broken sentences, inconsistent placeholders, duplicated
  redactions on the same span, identifier fields accidentally altered).
- Summarize recurring failure patterns per approach.

**Outcome:** a qualitative analysis document with annotated before/after
examples (synthetic data only), committed to the repository.

### 6.2 Quantitative Comparison and Metrics

Score every approach against the same synthetic dataset (which has known
ground-truth PII spans/labels, since it was generated) on at least the
following axes:

- **Anonymization effectiveness**: precision/recall/F1 of detected PII
  spans against ground truth, separately for structured fields and
  free-text documents (report both — they behave very differently).
- **Execution speed**: wall-clock time per record and throughput
  (records/second), measured on the same hardware, separating one-time
  setup/model-loading cost from steady-state per-record cost.
- **Resource footprint**: peak memory, whether a GPU is required or
  meaningfully helps, model size on disk.
- **Context-adaptability**: this is the most important axis, and needs a
  concrete rubric, not just an impression. Define a small number of
  **context profiles** (e.g. "record where certain fields carry important
  domain meaning," "generic administrative document," "public-facing
  report") and, for each profile, a policy for fields whose sensitivity is
  context-dependent — the canonical example: a date of birth is sensitive
  in general, but in a context where age is meaningful it may need to be
  *partially* preserved (e.g. truncated to year-only or month/year) rather
  than fully removed, whereas in another context full redaction is
  preferable. Score each approach on how easily/faithfully it supports such
  a context-specific policy (native support for partial redaction /
  generalization vs. all-or-nothing redaction vs. requiring custom code).
- **Consistency/determinism**: same input run twice — does the output
  match exactly? This matters for reproducibility and for any identifier
  that must stay stable across runs. Model-based approaches may not be
  perfectly deterministic; document this explicitly per approach.
- **Reversibility / re-identification risk** (qualitative note, not a hard
  metric): does the approach support pseudonymization (reversible with a
  key) versus pure irreversible redaction, and what that trade-off means
  when consistent-but-anonymous references are needed across documents.

**Outcome:** a reproducible benchmark (script or notebook) producing a
results table/CSV and one plot per axis, plus a written quantitative
analysis summarizing the numbers, both committed to the repository.

---

## 7. Synthesis and Recommendation

- Cross-reference the qualitative and quantitative findings into a single
  comparison matrix (rows = approaches, columns = metrics from Section
  6.2).
- Propose a **context-aware selection strategy**: e.g. a decision table or
  simple policy mapping (data context, field type) → (anonymization
  approach, field-level override), so the recommendation is directly
  actionable rather than purely theoretical.
- Explicitly flag open questions and risks for future work (e.g. deploying
  the chosen approach(es) against real, continuously arriving data,
  extending the common format to more input types, handling multi-language
  documents, or building a feedback loop where flagged edge cases improve
  anonymization rules over time).

**Outcome:** a final recommendation document, committed to the repository,
plus a short walkthrough/presentation of the findings.

---

## 8. Working Conventions

- **Never use real personal data** for any experiment, benchmark, or
  report example in this work. Use synthetic data only. If real sample
  data is ever needed to validate a finding, that must be discussed and
  approved with the supervisor first.
- A starter set of sample data will be provided to work from. Feel free to
  enrich it: generate additional synthetic data covering formats and
  structures not in the starter set (different delimiters/encodings,
  nested or semi-structured records, longer free-text documents, other
  languages, edge cases like partially missing fields) to stress-test the
  approaches more thoroughly.
- Keep the repository's `README.md` current at all times, and prefer many
  small, well-described commits over infrequent large ones — the commit
  history and README together should let anyone reconstruct what was done
  and why, at any point.
- Check in regularly with the supervisor to discuss progress, findings,
  and next steps; no need for long written status reports in between the
  README updates already required above.

