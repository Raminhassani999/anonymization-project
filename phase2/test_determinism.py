from pathlib import Path
import hashlib
import subprocess
import sys
import shutil


PHASE2_DIR = Path(__file__).resolve().parent
WIKI_FILE = PHASE2_DIR / "wiki" / "sources" / "smoke-test-source.md"
RUNS_DIR = PHASE2_DIR / "determinism_runs"

RUNS = 3


def calculate_hash(file_path):
    data = file_path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def main():
    hashes = []

    # Start with a clean directory
    if RUNS_DIR.exists():
        shutil.rmtree(RUNS_DIR)

    RUNS_DIR.mkdir()

    print("Running determinism test...")
    print(f"Runs: {RUNS}")
    print()

    for run in range(1, RUNS + 1):
        print(f"--- Run {run} ---")

        result = subprocess.run(
            [sys.executable, str(PHASE2_DIR / "ingest.py")],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:
            print("Ingest failed.")
            print(result.stderr)
            return

        if not WIKI_FILE.exists():
            print(f"Wiki file not found: {WIKI_FILE}")
            return

        # Calculate hash
        file_hash = calculate_hash(WIKI_FILE)
        hashes.append(file_hash)

        # Save a copy of this run
        run_file = RUNS_DIR / f"run_{run}.md"
        shutil.copy2(WIKI_FILE, run_file)

        print(f"SHA256: {file_hash}")
        print(f"Saved: {run_file}")
        print()

    print("=== Result ===")

    if len(set(hashes)) == 1:
        print("PASS: All runs produced identical wiki pages.")
    else:
        print("FAIL: The wiki pages are different between runs.")

        for i, file_hash in enumerate(hashes, start=1):
            print(f"Run {i}: {file_hash}")

        print()
        print(f"Saved outputs are in: {RUNS_DIR}")


if __name__ == "__main__":
    main()