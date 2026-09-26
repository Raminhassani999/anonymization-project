from pathlib import Path
import requests

SOURCE_FILE = Path("phase2/sources/smoke_source.md")
OUTPUT_FILE = Path("phase2/wiki/diabetes.md")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def main():
    source_text = SOURCE_FILE.read_text(encoding="utf-8")

    prompt = f"""
Read the following source and create a concise Markdown knowledge page.

The page must contain:
# Title
## Summary
## Key Facts

Only use information supported by the source.
Do not invent additional facts.

SOURCE:
{source_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()
    generated_page = result["response"]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        generated_page,
        encoding="utf-8"
    )

    print(f"Wiki page created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()