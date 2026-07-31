from normalization.universal_loader import load_any_file
from detection.regex_detector import detect_dataframe
if __name__ == "__main__":
    file_path = "data/diabetology/diabetology-synthetic-dataset.xlsx"

    data = load_any_file(file_path)
    pii_results = detect_dataframe(data["content"])

    print("Detected PII:")

    for item in pii_results:
        print(item)