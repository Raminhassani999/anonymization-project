from pathlib import Path
from datetime import datetime
import hashlib
import json
import re
import time

import requests


# ============================================================
# CONFIGURATION
# ============================================================

PHASE2_DIR = Path("phase2")

SCHEMA_FILE = PHASE2_DIR / "schema.md"
INDEX_FILE = PHASE2_DIR / "wiki" / "index.md"
LOG_FILE = PHASE2_DIR / "wiki" / "log.md"

SOURCE_FILE = PHASE2_DIR / "sources" / "smoke_source.md"

SOURCE_PAGES_DIR = (
    PHASE2_DIR
    / "wiki"
    / "sources"
)

# ------------------------------------------------------------
# IMPORTANT
#
# False:
#   Reuse an existing wiki page when the source is unchanged.
#
# True:
#   Force Ollama to regenerate the wiki page.
#
# Keep this False for normal/idempotent ingestion.
# ------------------------------------------------------------

FORCE_REINGEST = False


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

MODEL = "qwen3:4b"

QUANTIZATION = "Q4_K_M"

PROMPT_VERSION = "schema-v1"


# ============================================================
# TEXT UTILITIES
# ============================================================

def normalize_text(text):
    """
    Normalize whitespace and case for comparisons.
    """

    return " ".join(
        text.lower().split()
    )


def slugify(text):
    """
    Convert a title into a stable lowercase filename.
    """

    text = text.lower().strip()

    text = re.sub(
        r"[^a-z0-9]+",
        "-",
        text
    )

    return text.strip("-")


def render_list(items):
    """
    Render a list of strings as Markdown bullets.

    Empty lists are represented explicitly.
    """

    if not items:
        return "None identified."

    return "\n".join(
        f"- {item}"
        for item in items
    )


def calculate_sha256(text):
    """
    Calculate a stable SHA-256 hash for source content.
    """

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# ============================================================
# SOURCE PROCESSING
# ============================================================

def extract_source_title(source_text):
    """
    Extract the first Markdown H1 heading.

    Example:

        # Smoke Test Source

    becomes:

        Smoke Test Source
    """

    for line in source_text.splitlines():

        line = line.strip()

        if line.startswith("# "):

            title = line[2:].strip()

            if title:
                return title

    return "Untitled Source"


def extract_source_facts(source_text):
    """
    Extract every non-empty, non-heading line
    from the immutable source.

    These facts become the final claims directly.
    """

    facts = []

    for line in source_text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        facts.append(line)

    return facts


# ============================================================
# EXISTING WIKI PAGE
# ============================================================

def extract_existing_source_hash(wiki_text):
    """
    Extract the source SHA-256 hash from an existing
    wiki page.

    The hash is stored in an HTML comment:

        <!-- source_sha256: abc123 -->

    Returns:
        hash string
        or None if not found
    """

    pattern = (
        r"<!--\s*source_sha256:\s*"
        r"([a-fA-F0-9]{64})\s*-->"
    )

    match = re.search(
        pattern,
        wiki_text
    )

    if match:
        return match.group(1)

    return None


def existing_page_matches_source(
    output_file,
    source_hash
):
    """
    Determine whether an existing wiki page was
    generated from the exact same source content.
    """

    if not output_file.exists():
        return False

    existing_text = output_file.read_text(
        encoding="utf-8"
    )

    existing_hash = extract_existing_source_hash(
        existing_text
    )

    if existing_hash is None:
        return False

    return existing_hash == source_hash


# ============================================================
# VALIDATION
# ============================================================

def validate_source_data(data):
    """
    Validate the final structured data.
    """

    required_fields = [
        "title",
        "summary",
        "key_facts",
        "entities",
        "concepts",
        "claims",
        "source_reference"
    ]

    missing = [
        field
        for field in required_fields
        if field not in data
    ]

    if missing:

        raise ValueError(
            "Model response is missing required fields:\n"
            + "\n".join(missing)
        )

    if not isinstance(
        data["title"],
        str
    ):
        raise ValueError(
            "title must be a string"
        )

    if not isinstance(
        data["summary"],
        str
    ):
        raise ValueError(
            "summary must be a string"
        )

    if not isinstance(
        data["key_facts"],
        list
    ):
        raise ValueError(
            "key_facts must be a list"
        )

    if not isinstance(
        data["entities"],
        list
    ):
        raise ValueError(
            "entities must be a list"
        )

    if not isinstance(
        data["concepts"],
        list
    ):
        raise ValueError(
            "concepts must be a list"
        )

    if not isinstance(
        data["claims"],
        list
    ):
        raise ValueError(
            "claims must be a list"
        )

    if not isinstance(
        data["source_reference"],
        str
    ):
        raise ValueError(
            "source_reference must be a string"
        )

    for field in [
        "key_facts",
        "entities",
        "concepts",
        "claims"
    ]:

        for item in data[field]:

            if not isinstance(
                item,
                str
            ):

                raise ValueError(
                    f"{field} must contain only strings"
                )


# ============================================================
# PROMPT
# ============================================================

def build_prompt(
    source_text,
    schema_text,
    index_text
):
    """
    Build the prompt sent to Ollama.

    The model generates semantic information only.

    Python generates deterministic metadata:

        - title
        - source_reference
        - claims
        - source hash
    """

    prompt = f"""
You are maintaining a persistent knowledge wiki.

Your task is to analyze the SOURCE DOCUMENT and
produce structured semantic information about it.

The source document is authoritative.

Use ONLY information supported by the source.

SCHEMA INFORMATION
--------------------
{schema_text}
--------------------

CURRENT WIKI INDEX
--------------------
{index_text}
--------------------

SOURCE DOCUMENT
--------------------
{source_text}
--------------------

Return ONLY ONE valid JSON object.

The JSON object MUST contain exactly these fields:

{{
  "summary": "string",
  "key_facts": ["string"],
  "entities": ["string"],
  "concepts": ["string"]
}}

IMPORTANT:

- Return valid JSON only.
- Do not use Markdown.
- Do not use ```json fences.
- Do not add explanations.
- Do not add text before or after the JSON object.

CLAIM RULE:

Claims are controlled by Python.

DO NOT generate a claims field.

Python will copy every factual statement from
the immutable source document directly into the
final claims list.

OTHER RULES:

- Use only information supported by the source.
- Do not invent facts.
- The summary must actually summarize this source.
- Key facts should reflect important content.
- Entities should be concrete named entities when supported.
- Concepts should represent general ideas, conditions,
  processes, methods, properties, or definitions.
- Do not place the same item in both entities and concepts.
- Do not create entities merely because a concept exists.
- Do not add synonyms or unsupported information.
- Do not copy the schema into the response.
- Do not copy the wiki index into the response.

CLASSIFICATION RULES:

- A specific identifiable object, actor, organization,
  dataset, tool, software system, artifact, cohort,
  or named object is an entity.
- A general disease, condition, method, process,
  property, definition, measurement concept,
  or domain principle is a concept.
- For this smoke-test source, Diabetes,
  Type 2 diabetes, and Insulin resistance are concepts.
- Do not classify general diseases or medical conditions
  as entities.
"""

    return prompt


# ============================================================
# OLLAMA
# ============================================================

def call_ollama(prompt):
    """
    Call Ollama and return:

        structured_data
        elapsed_seconds
    """

    start_time = time.perf_counter()

    response = requests.post(
        OLLAMA_URL,

        json={

            "model": MODEL,

            "prompt": prompt,

            "stream": False,

            # Force structured JSON output.
            "format": {

                "type": "object",

                "properties": {

                    "summary": {
                        "type": "string"
                    },

                    "key_facts": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "entities": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },

                    "concepts": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },

                "required": [
                    "summary",
                    "key_facts",
                    "entities",
                    "concepts"
                ]
            },

            "options": {

                # Deterministic generation settings.
                "temperature": 0,
                "seed": 42,

                # Reduce sampling variability.
                "top_k": 1,
                "top_p": 1
            }
        },

        timeout=300
    )

    response.raise_for_status()

    elapsed_seconds = (
        time.perf_counter()
        - start_time
    )

    response_json = response.json()

    raw_model_response = response_json.get(
        "response",
        ""
    )

    print(
        "=== RAW OLLAMA RESPONSE ==="
    )

    print(
        repr(raw_model_response)
    )

    print(
        "=== END RAW OLLAMA RESPONSE ==="
    )

    if not raw_model_response.strip():

        raise ValueError(
            "Ollama returned an empty response."
        )

    try:

        structured_data = json.loads(
            raw_model_response
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Ollama returned invalid JSON:\n"
            + raw_model_response
        ) from error

    return (
        structured_data,
        elapsed_seconds
    )


# ============================================================
# WIKI PAGE RENDERING
# ============================================================

def render_source_page(
    title,
    data,
    source_reference,
    source_hash
):
    """
    Build the Markdown source page deterministically.

    The source hash allows future ingests to determine
    whether the source content has actually changed.
    """

    summary = data["summary"]

    key_facts = render_list(
        data["key_facts"]
    )

    entities = render_list(
        data["entities"]
    )

    concepts = render_list(
        data["concepts"]
    )

    claims = render_list(
        data["claims"]
    )

    return f"""# {title}

<!-- source_sha256: {source_hash} -->

## Summary

{summary}

## Key Facts

{key_facts}

## Entities

{entities}

## Concepts

{concepts}

## Claims

{claims}

## Source Reference

{source_reference}
"""


# ============================================================
# INDEX
# ============================================================

def update_index(
    title,
    summary,
    relative_path
):
    """
    Update wiki/index.md as a content-oriented catalog.

    The same page may appear only once.

    Existing entries pointing to the same relative path
    are removed before the canonical entry is added.

    This makes repeated ingestion idempotent.
    """

    INDEX_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if INDEX_FILE.exists():

        index_text = INDEX_FILE.read_text(
            encoding="utf-8"
        )

    else:

        index_text = """# Knowledge Wiki Index

This is the content-oriented catalog of the knowledge wiki.

## Sources

No sources indexed yet.

## Entities

No entity pages yet.

## Concepts

No concept pages yet.

## Analyses

No analysis pages yet.

## Overview

No overview page yet.

## Glossary

No glossary page yet.
"""

    # --------------------------------------------------------
    # Remove every existing entry for this exact page.
    # --------------------------------------------------------

    lines = index_text.splitlines()

    filtered_lines = []

    for line in lines:

        stripped = line.strip()

        if (
            stripped.startswith("- [")
            and f"]({relative_path})" in stripped
        ):
            continue

        filtered_lines.append(line)

    index_text = "\n".join(
        filtered_lines
    )

    # --------------------------------------------------------
    # Remove obsolete placeholder.
    # --------------------------------------------------------

    index_text = index_text.replace(
        "No sources indexed yet.\n",
        ""
    )

    # --------------------------------------------------------
    # Remove excessive blank lines.
    # --------------------------------------------------------

    while "\n\n\n" in index_text:

        index_text = index_text.replace(
            "\n\n\n",
            "\n\n"
        )

    # --------------------------------------------------------
    # Canonical entry.
    # --------------------------------------------------------

    index_entry = (
        f"- [{title}]({relative_path}) - {summary}"
    )

    # --------------------------------------------------------
    # Insert into Sources section.
    # --------------------------------------------------------

    marker = "## Sources"

    if marker in index_text:

        parts = index_text.split(
            marker,
            1
        )

        before_sources = parts[0]

        after_sources = parts[1]

        after_sources = (
            "\n\n"
            + index_entry
            + "\n"
            + after_sources.lstrip("\n")
        )

        index_text = (
            before_sources
            + marker
            + after_sources
        )

    else:

        index_text = (
            index_text.rstrip()
            + "\n\n## Sources\n\n"
            + index_entry
            + "\n"
        )

    # --------------------------------------------------------
    # Final normalization.
    # --------------------------------------------------------

    index_text = (
        index_text.rstrip()
        + "\n"
    )

    INDEX_FILE.write_text(
        index_text,
        encoding="utf-8"
    )


# ============================================================
# LOG
# ============================================================

def append_log(
    elapsed_seconds,
    output_file,
    reused_existing_page=False
):
    """
    Append an ingest operation to wiki/log.md.
    """

    LOG_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if reused_existing_page:

        operation_status = (
            "reused_existing_page"
        )

    else:

        operation_status = "success"

    entry = f"""
## [{timestamp}] ingest | smoke_source

- operation: ingest
- source: sources/smoke_source.md
- model: {MODEL}
- quantization: {QUANTIZATION}
- prompt_version: {PROMPT_VERSION}
- temperature: 0
- seed: 42
- top_k: 1
- top_p: 1
- output: {output_file.as_posix()}
- latency_seconds: {elapsed_seconds:.3f}
- status: {operation_status}
"""

    with LOG_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            entry
        )


# ============================================================
# MAIN INGEST PIPELINE
# ============================================================

def main():

    # --------------------------------------------------------
    # 1. Read source
    # --------------------------------------------------------

    if not SOURCE_FILE.exists():

        raise FileNotFoundError(
            f"Source file not found: {SOURCE_FILE}"
        )

    source_text = SOURCE_FILE.read_text(
        encoding="utf-8"
    )

    if not source_text.strip():

        raise ValueError(
            "Source file is empty."
        )

    source_facts = extract_source_facts(
        source_text
    )

    if not source_facts:

        raise ValueError(
            "No source facts were extracted."
        )

    # --------------------------------------------------------
    # 2. Determine deterministic metadata
    # --------------------------------------------------------

    title = extract_source_title(
        source_text
    )

    source_reference = (
        SOURCE_FILE.as_posix()
    )

    source_hash = calculate_sha256(
        source_text
    )

    slug = slugify(
        title
    )

    SOURCE_PAGES_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        SOURCE_PAGES_DIR
        / f"{slug}.md"
    )

    relative_path = (
        f"sources/{output_file.name}"
    )

    # --------------------------------------------------------
    # 3. Check whether this exact source was already ingested
    # --------------------------------------------------------

    if (
        not FORCE_REINGEST
        and existing_page_matches_source(
            output_file,
            source_hash
        )
    ):

        print(
            "Existing wiki page matches the current source."
        )

        print(
            "Skipping Ollama regeneration."
        )

        print(
            "This preserves idempotence."
        )

        # Read existing page to obtain its summary
        # for the index.

        existing_text = output_file.read_text(
            encoding="utf-8"
        )

        summary_match = re.search(
            r"## Summary\s*\n\n(.*?)\n\n## Key Facts",
            existing_text,
            re.DOTALL
        )

        if summary_match:

            summary = (
                summary_match.group(1).strip()
            )

        else:

            summary = (
                "Existing source page."
            )

        # Update index without changing the wiki page.

        update_index(
            title,
            summary,
            relative_path
        )

        # No LLM call happened.

        append_log(
            0.0,
            output_file,
            reused_existing_page=True
        )

        print(
            f"Ingest completed: "
            f"{output_file.as_posix()}"
        )

        print(
            "Mode: reused existing canonical page"
        )

        print(
            "Claims: preserved from existing page."
        )

        print(
            "Index: duplicate-safe update completed."
        )

        return

    # --------------------------------------------------------
    # 4. Read schema
    # --------------------------------------------------------

    if not SCHEMA_FILE.exists():

        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_FILE}"
        )

    schema_text = SCHEMA_FILE.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # 5. Read existing index
    # --------------------------------------------------------

    if INDEX_FILE.exists():

        index_text = INDEX_FILE.read_text(
            encoding="utf-8"
        )

    else:

        index_text = (
            "No wiki index exists yet."
        )

    # --------------------------------------------------------
    # 6. Build prompt
    # --------------------------------------------------------

    prompt = build_prompt(
        source_text,
        schema_text,
        index_text
    )

    print(
        "=== PROMPT SENT TO OLLAMA ==="
    )

    # ASCII-safe console output.
    print(
        prompt.encode(
            "ascii",
            errors="replace"
        ).decode("ascii")
    )

    print(
        "=== END PROMPT ==="
    )

    # --------------------------------------------------------
    # 7. Call Ollama
    # --------------------------------------------------------

    structured_data, elapsed_seconds = (
        call_ollama(prompt)
    )

    # --------------------------------------------------------
    # 8. Force deterministic metadata and claims
    # --------------------------------------------------------

    # Python owns these fields.

    structured_data["title"] = title

    structured_data["source_reference"] = (
        source_reference
    )

    # Claims come DIRECTLY from the immutable source.

    structured_data["claims"] = (
        source_facts.copy()
    )

    # --------------------------------------------------------
    # 9. Validate final structure
    # --------------------------------------------------------

    validate_source_data(
        structured_data
    )

    # --------------------------------------------------------
    # 10. Render wiki page
    # --------------------------------------------------------

    wiki_page = render_source_page(
        title,
        structured_data,
        source_reference,
        source_hash
    )

    # --------------------------------------------------------
    # 11. Write wiki page
    # --------------------------------------------------------

    output_file.write_text(
        wiki_page,
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # 12. Update index
    # --------------------------------------------------------

    update_index(
        title,
        structured_data["summary"],
        relative_path
    )

    # --------------------------------------------------------
    # 13. Append log
    # --------------------------------------------------------

    append_log(
        elapsed_seconds,
        output_file,
        reused_existing_page=False
    )

    # --------------------------------------------------------
    # 14. Report
    # --------------------------------------------------------

    print(
        f"Ingest completed: "
        f"{output_file.as_posix()}"
    )

    print(
        f"Model: {MODEL}"
    )

    print(
        f"Latency: "
        f"{elapsed_seconds:.3f} seconds"
    )

    print(
        "Claims: copied directly from source."
    )

    print(
        "Index: duplicate-safe update completed."
    )

    print(
        f"Source SHA256: {source_hash}"
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except Exception:

        print(
            "\nIngest failed."
        )

        raise