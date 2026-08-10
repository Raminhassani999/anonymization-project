from detection.spacy_detector import SpacyDetector
from detection.hf_detector_class import HuggingFaceDetector
from detection.gliner_detector_class import GlinerDetector
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
    return LABEL_MAP.get(label, label)


def get_predictions(detector, text):

    predictions = detector.detect(text)

    result = []

    for prediction in predictions:

        value = prediction["value"]
        entity_type = normalize_label(
            prediction["entity"]
        )

        start = prediction.get("start")
        end = prediction.get("end")

        # Fallback for detectors that do not provide spans
        if start is None or end is None:

            start = text.find(value)

            if start == -1:
                continue

            end = start + len(value)

        result.append({
            "value": value,
            "entity": entity_type,
            "start": start,
            "end": end
        })

    return result


def get_ground_truth(entities):

    result = []

    for entity in entities:

        result.append({
            "value": entity["value"],
            "entity": normalize_label(
                entity["entity"]
            ),
            "start": entity["start"],
            "end": entity["end"]
        })

    return result


def analyze_detector(detector, dataset):

    false_positives = []
    false_negatives = []
    boundary_errors = []
    type_errors = []

    for example in dataset:

        text = example["text"]

        predictions = get_predictions(
            detector,
            text
        )

        expected = get_ground_truth(
            example["entities"]
        )

        matched_predictions = set()
        matched_expected = set()

        # ------------------------------------------------
        # 1. Exact matches
        # ------------------------------------------------

        for prediction_index, prediction in enumerate(predictions):

            prediction_key = (
                prediction["start"],
                prediction["end"],
                prediction["entity"]
            )

            for expected_index, entity in enumerate(expected):

                expected_key = (
                    entity["start"],
                    entity["end"],
                    entity["entity"]
                )

                if prediction_key == expected_key:

                    matched_predictions.add(
                        prediction_index
                    )

                    matched_expected.add(
                        expected_index
                    )

                    break

        # ------------------------------------------------
        # 2. Analyze unmatched predictions
        # ------------------------------------------------

        for prediction_index, prediction in enumerate(predictions):

            if prediction_index in matched_predictions:
                continue

            found_error = False

            # Check for same span but wrong entity type
            for expected_index, entity in enumerate(expected):

                if expected_index in matched_expected:
                    continue

                same_span = (
                    prediction["start"] == entity["start"]
                    and
                    prediction["end"] == entity["end"]
                )

                if same_span:

                    type_errors.append({
                        "text": text,
                        "value": prediction["value"],
                        "predicted_entity": prediction["entity"],
                        "expected_entity": entity["entity"],
                        "start": prediction["start"],
                        "end": prediction["end"]
                    })

                    matched_predictions.add(
                        prediction_index
                    )

                    matched_expected.add(
                        expected_index
                    )

                    found_error = True

                    break

            if found_error:
                continue

            # Check for overlapping spans
            for expected_index, entity in enumerate(expected):

                if expected_index in matched_expected:
                    continue

                prediction_overlaps = (
                    prediction["start"] < entity["end"]
                    and
                    prediction["end"] > entity["start"]
                )

                if prediction_overlaps:

                    boundary_errors.append({
                        "text": text,
                        "predicted_value": prediction["value"],
                        "expected_value": entity["value"],
                        "entity": prediction["entity"],
                        "expected_entity": entity["entity"],
                        "predicted_start": prediction["start"],
                        "predicted_end": prediction["end"],
                        "expected_start": entity["start"],
                        "expected_end": entity["end"]
                    })

                    matched_predictions.add(
                        prediction_index
                    )

                    matched_expected.add(
                        expected_index
                    )

                    found_error = True

                    break

            if found_error:
                continue

            # Otherwise it is a genuine false positive
            false_positives.append({
                "text": text,
                "value": prediction["value"],
                "entity": prediction["entity"],
                "start": prediction["start"],
                "end": prediction["end"]
            })

        # ------------------------------------------------
        # 3. Remaining expected entities are false negatives
        # ------------------------------------------------

        for expected_index, entity in enumerate(expected):

            if expected_index in matched_expected:
                continue

            false_negatives.append({
                "text": text,
                "value": entity["value"],
                "entity": entity["entity"],
                "start": entity["start"],
                "end": entity["end"]
            })

    return {
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "boundary_errors": boundary_errors,
        "type_errors": type_errors
    }


def print_errors(title, errors):

    print(f"\n--- {title} ---")

    if not errors:
        print("None")
        return

    for error in errors:

        print(error)


if __name__ == "__main__":

    detectors = {
        "spaCy": SpacyDetector(),
        "Hugging Face": HuggingFaceDetector(),
        "GLiNER": GlinerDetector()
    }

    for name, detector in detectors.items():

        print(f"\n{'=' * 5} {name} {'=' * 5}")

        results = analyze_detector(
            detector,
            GROUND_TRUTH
        )

        print_errors(
            "FALSE POSITIVES",
            results["false_positives"]
        )

        print_errors(
            "FALSE NEGATIVES",
            results["false_negatives"]
        )

        print_errors(
            "BOUNDARY ERRORS",
            results["boundary_errors"]
        )

        print_errors(
            "TYPE ERRORS",
            results["type_errors"]
        )