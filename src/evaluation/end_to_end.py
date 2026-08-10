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


def get_ground_truth_detections(example):
    """
    Convert ground-truth entities into the format
    expected by the text anonymizer.
    """

    detections = []

    for entity in example["entities"]:

        detections.append({
            "start": entity["start"],
            "end": entity["end"],
            "entity": normalize_label(
                entity["entity"]
            )
        })

    return detections


def evaluate_end_to_end(detector, dataset):

    total_examples = len(dataset)

    exact_output_matches = 0

    total_ground_truth_entities = 0
    anonymized_entities = 0
    remaining_pii = 0

    for example in dataset:

        text = example["text"]

        # ----------------------------------------
        # Ground-truth anonymized output
        # ----------------------------------------

        ground_truth_detections = (
            get_ground_truth_detections(
                example
            )
        )

        expected_output = anonymize_text(
            text,
            ground_truth_detections
        )

        # ----------------------------------------
        # Model predictions
        # ----------------------------------------

        predictions = detector.detect(text)

        predicted_detections = []

        for prediction in predictions:

            if (
                "start" not in prediction
                or "end" not in prediction
            ):
                continue

            predicted_detections.append({
                "start": prediction["start"],
                "end": prediction["end"],
                "entity": normalize_label(
                    prediction["entity"]
                )
            })

        # ----------------------------------------
        # Model anonymized output
        # ----------------------------------------

        actual_output = anonymize_text(
            text,
            predicted_detections
        )

        # ----------------------------------------
        # Exact output comparison
        # ----------------------------------------

        if actual_output == expected_output:

            exact_output_matches += 1

        # ----------------------------------------
        # Entity-level anonymization analysis
        # ----------------------------------------

        total_ground_truth_entities += len(
            example["entities"]
        )

        for entity in example["entities"]:

            original_value = entity["value"]

            start = entity["start"]
            end = entity["end"]

            # Check whether the exact ground-truth
            # span was predicted.
            matched = False

            for prediction in predicted_detections:

                if (
                    prediction["start"] == start
                    and
                    prediction["end"] == end
                    and
                    normalize_label(
                        prediction["entity"]
                    )
                    ==
                    normalize_label(
                        entity["entity"]
                    )
                ):

                    matched = True
                    break

            if matched:

                anonymized_entities += 1

            # Check whether the original PII value
            # still appears at its original location.
            if (
                actual_output[start:end]
                == original_value
            ):

                remaining_pii += 1

    exact_match_rate = (
        exact_output_matches / total_examples
        if total_examples > 0
        else 0
    )

    anonymization_rate = (
        anonymized_entities
        / total_ground_truth_entities
        if total_ground_truth_entities > 0
        else 0
    )

    return {
        "examples": total_examples,
        "ground_truth_entities":
            total_ground_truth_entities,
        "anonymized_entities":
            anonymized_entities,
        "remaining_pii":
            remaining_pii,
        "exact_output_matches":
            exact_output_matches,
        "exact_match_rate":
            exact_match_rate,
        "anonymization_rate":
            anonymization_rate
    }


def print_results(results):

    print(
        f"Number of examples: "
        f"{results['examples']}"
    )

    print(
        f"Ground-truth entities: "
        f"{results['ground_truth_entities']}"
    )

    print(
        f"Correctly anonymized entities: "
        f"{results['anonymized_entities']}"
    )

    print(
        f"Remaining PII entities: "
        f"{results['remaining_pii']}"
    )

    print(
        f"Exact anonymized outputs: "
        f"{results['exact_output_matches']}"
    )

    print(
        f"Entity anonymization rate: "
        f"{results['anonymization_rate']:.3f}"
    )

    print(
        f"Exact output match rate: "
        f"{results['exact_match_rate']:.3f}"
    )


if __name__ == "__main__":

    detectors = {
        "spaCy": SpacyDetector(),
        "Hugging Face": HuggingFaceDetector(),
        "GLiNER": GlinerDetector()
    }

    for name, detector in detectors.items():

        print(
            f"\n===== {name} ====="
        )

        results = evaluate_end_to_end(
            detector,
            GROUND_TRUTH
        )

        print_results(results)