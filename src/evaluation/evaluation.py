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
    "date": "date"
}


def normalize_label(label):
    return LABEL_MAP.get(label, label.lower())


def evaluate_detector(detector, dataset):

    true_positive = 0
    false_positive = 0
    false_negative = 0

    for example in dataset:

        text = example["text"]
        ground_truth = example["entities"]

        predictions = detector.detect(text)

        predicted_entities = set()

        for prediction in predictions:

            value = prediction["value"]

            entity_type = normalize_label(
                prediction["entity"]
            )

            start = prediction["start"]
            end = prediction["end"]

            predicted_entities.add(
                (
                    start,
                    end,
                    entity_type
                )
            )

        expected_entities = set()

        for entity in ground_truth:

            expected_entities.add(
                (
                    entity["start"],
                    entity["end"],
                    normalize_label(
                        entity["entity"]
                    )
                )
            )

        true_positive += len(
            predicted_entities & expected_entities
        )

        false_positive += len(
            predicted_entities - expected_entities
        )

        false_negative += len(
            expected_entities - predicted_entities
        )

    # Precision
    if true_positive + false_positive > 0:

        precision = true_positive / (
            true_positive + false_positive
        )

    else:

        precision = 0

    # Recall
    if true_positive + false_negative > 0:

        recall = true_positive / (
            true_positive + false_negative
        )

    else:

        recall = 0

    # F1
    if precision + recall > 0:

        f1 = 2 * (
            precision * recall
        ) / (
            precision + recall
        )

    else:

        f1 = 0

    return {
        "TP": true_positive,
        "FP": false_positive,
        "FN": false_negative,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


if __name__ == "__main__":

    detectors = {
        "spaCy": SpacyDetector(),
        "Hugging Face": HuggingFaceDetector(),
        "GLiNER": GlinerDetector()
    }

    for name, detector in detectors.items():

        print(f"\n===== {name} =====")

        results = evaluate_detector(
            detector,
            GROUND_TRUTH
        )

        print(f"TP: {results['TP']}")
        print(f"FP: {results['FP']}")
        print(f"FN: {results['FN']}")
        print(f"Precision: {results['precision']:.3f}")
        print(f"Recall: {results['recall']:.3f}")
        print(f"F1: {results['f1']:.3f}")