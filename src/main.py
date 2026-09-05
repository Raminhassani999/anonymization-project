from normalization.universal_loader import load_any_file
from detection.detection_engine import detect_all
from anonymization.rule_based_anonymizer import anonymize_dataframe
from anonymization.text_anonymizer import anonymize_text

DETECTOR = "spacy"

NER_COLUMNS = []


if __name__ == "__main__":

    file_path = "data/diabetology/diabetology-synthetic-dataset.xlsx"

    data = load_any_file(file_path)

    # Detect PII in both:
    # 1. structured columns using Regex
    # 2. columns listed in NER_COLUMNS using the selected NER model
    pii_results = detect_all(
        data["content"],
        detector=DETECTOR
    )

    # Anonymize the structured PII
    anonymised_df = anonymize_dataframe(
        data["content"],
        pii_results
    )

    # Anonymize free-text NER columns
    for column in NER_COLUMNS:

        if column not in data["content"].columns:
            continue

        for row in data["content"].index:

            text = str(data["content"].at[row, column])

            # Get only the NER detections belonging to
            # this particular cell
            text_detections = [
                detection
                for detection in pii_results
                if detection.get("row") == row
                and detection.get("column") == column
                and "start" in detection
                and "end" in detection
            ]

            # Replace the detected entities in the text
            anonymised_df.at[row, column] = anonymize_text(
                text,
                text_detections
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