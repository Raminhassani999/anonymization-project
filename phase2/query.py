from pathlib import Path
import requests

WIKI_FILE = Path("phase2/wiki/diabetes.md")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"


def main():
    wiki_text = WIKI_FILE.read_text(encoding="utf-8")

    question = "What is Type 2 diabetes associated with?"

    prompt = f"""
Answer the question using only the information in the wiki below.

WIKI:
{wiki_text}

QUESTION:
{question}

Give a concise answer.
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

    answer = response.json()["response"]

    print("Question:")
    print(question)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()