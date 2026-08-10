from normalization.universal_loader import load_any_file
from detection.detection_engine import detect_all
from anonymization.rule_based_anonymizer import anonymize_dataframe
DETECTOR = "spacy"

if __name__ == "__main__":

    file_path = "data/diabetology/diabetology-synthetic-dataset.xlsx"

    data = load_any_file(file_path)

    pii_results = detect_all(
        data["content"],
        detector=DETECTOR
    )

    anonymised_df = anonymize_dataframe(
        data["content"],
        pii_results
    )

    output_file = "output/anonymized_dataset.xlsx"

    anonymised_df.to_excel(
        output_file,
        index=False
    )

    print(
        f"\nAnonymized dataset saved to: {output_file}"
    )

    print(
        anonymised_df[
            [
                "Patient Code",
                "Tax Code",
                "Birth Date",
                "Assessment Date",
                "Age At Assessment"
            ]
        ].head()
    )