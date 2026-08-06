from normalization.universal_loader import load_any_file
from detection.regex_detector import detect_dataframe
from anonymization.rule_based_anonymizer import anonymize_dataframe
if __name__ == "__main__":
    file_path = "data/diabetology/diabetology-synthetic-dataset.xlsx"

    data = load_any_file(file_path)
    pii_results = detect_dataframe(data["content"])
    
    anonymised_df = anonymize_dataframe(data["content"] , pii_results , method = "generalize")

    print(
    anonymised_df[
        [
            "Birth Date",
            "Assessment Date",
            "Age At Assessment"
        ]
    ].head()
)