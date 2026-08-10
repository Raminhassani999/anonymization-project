from detection.spacy_detector import SpacyDetector
from detection.hf_detector_class import HuggingFaceDetector
from detection.gliner_detector_class import GlinerDetector

from anonymization.text_anonymizer import anonymize_text

from evaluation.ground_truth import GROUND_TRUTH


LABEL_MAP = {
    "PERSON": "person",
    "PER": "person",
    "ORG": "organization",
    "GPE": "location",
    "LOC": "location",
    "DATE": "date",
    "MISC": "misc",

    "person": "person",
    "organization": "organization",
    "location": "location",
    "date": "date",
    "misc": "misc"
}


def normalize_label(label):
    return LABEL_MAP.get(
        label,
        label.lower()
    )


def get_expected_detections(example):

    return [
        {
            "start": entity["start"],
            "end": entity["end"],
            "entity": normalize_label(
                entity["entity"]
            )
        }
        for entity in example["entities"]
    ]


def get_predictions(detector, text):

    predictions = detector.detect(text)

    result = []

    for prediction in predictions:

        if (
            "start" not in prediction
            or "end" not in prediction
        ):
            continue

        result.append({
            "start": prediction["start"],
            "end": prediction["end"],
            "entity": normalize_label(
                prediction["entity"]
            ),
            "value": prediction.get(
                "value",
                text[
                    prediction["start"]:
                    prediction["end"]
                ]
            )
        })

    return result


def analyze_example(
    detector,
    example
):

    text = example["text"]

    expected_detections = (
        get_expected_detections(example)
    )

    predictions = get_predictions(
        detector,
        text
    )

    expected_output = anonymize_text(
        text,
        expected_detections
    )

    actual_output = anonymize_text(
        text,
        predictions
    )

    return (
        expected_output,
        actual_output,
        expected_detections,
        predictions
    )


def classify_errors(
    expected_detections,
    predictions
):

    expected_set = {
        (
            item["start"],
            item["end"],
            item["entity"]
        )
        for item in expected_detections
    }

    predicted_set = {
        (
            item["start"],
            item["end"],
            item["entity"]
        )
        for item in predictions
    }

    false_negatives = (
        expected_set - predicted_set
    )

    false_positives = (
        predicted_set - expected_set
    )

    boundary_errors = []

    type_errors = []

    for expected in expected_detections:

        expected_start = expected["start"]
        expected_end = expected["end"]
        expected_type = expected["entity"]

        for prediction in predictions:

            predicted_start = prediction["start"]
            predicted_end = prediction["end"]
            predicted_type = prediction["entity"]

            same_span = (
                expected_start == predicted_start
                and
                expected_end == predicted_end
            )

            same_type = (
                expected_type == predicted_type
            )

            if same_span and not same_type:

                type_errors.append({
                    "expected": expected,
                    "predicted": prediction
                })

            elif (
                not same_span
                and
                (
                    max(
                        expected_start,
                        predicted_start
                    )
                    <
                    min(
                        expected_end,
                        predicted_end
                    )
                )
            ):

                boundary_errors.append({
                    "expected": expected,
                    "predicted": prediction
                })

    return (
        false_negatives,
        false_positives,
        boundary_errors,
        type_errors
    )


def run_analysis(
    detector,
    dataset
):

    failures = []

    for example in dataset:

        (
            expected_output,
            actual_output,
            expected_detections,
            predictions
        ) = analyze_example(
            detector,
            example
        )

        if expected_output != actual_output:

            (
                false_negatives,
                false_positives,
                boundary_errors,
                type_errors
            ) = classify_errors(
                expected_detections,
                predictions
            )

            failures.append({
                "text": example["text"],
                "expected_output": expected_output,
                "actual_output": actual_output,
                "false_negatives": false_negatives,
                "false_positives": false_positives,
                "boundary_errors": boundary_errors,
                "type_errors": type_errors
            })

    return failures


def print_failure(
    index,
    failure
):

    print(
        f"\n===== FAILURE {index} ====="
    )

    print(
        f"\nOriginal:\n"
        f"{failure['text']}"
    )

    print(
        f"\nExpected anonymized output:\n"
        f"{failure['expected_output']}"
    )

    print(
        f"\nActual anonymized output:\n"
        f"{failure['actual_output']}"
    )

    print(
        "\n--- FALSE NEGATIVES ---"
    )

    if failure["false_negatives"]:

        for item in failure["false_negatives"]:

            print(item)

    else:

        print("None")

    print(
        "\n--- FALSE POSITIVES ---"
    )

    if failure["false_positives"]:

        for item in failure["false_positives"]:

            print(item)

    else:

        print("None")

    print(
        "\n--- BOUNDARY ERRORS ---"
    )

    if failure["boundary_errors"]:

        for item in failure["boundary_errors"]:

            print(item)

    else:

        print("None")

    print(
        "\n--- TYPE ERRORS ---"
    )

    if failure["type_errors"]:

        for item in failure["type_errors"]:

            print(item)

    else:

        print("None")


if __name__ == "__main__":

    detectors = {
        "spaCy": SpacyDetector(),
        "Hugging Face": HuggingFaceDetector(),
        "GLiNER": GlinerDetector()
    }

    for name, detector in detectors.items():

        print(
            f"\n\n{'=' * 5} {name} {'=' * 5}"
        )

        failures = run_analysis(
            detector,
            GROUND_TRUTH
        )

        print(
            f"\nTotal failed anonymized outputs: "
            f"{len(failures)}"
        )

        for index, failure in enumerate(
            failures,
            start=1
        ):

            print_failure(
                index,
                failure
            )