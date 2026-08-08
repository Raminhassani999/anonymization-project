from detection.spacy_detector import SpacyDetector
from detection.hf_detector_class import HuggingFaceDetector
from detection.gliner_detector_class import GlinerDetector


text = """
Mario Rossi visited Policlinico di Messina in Italy.
Luigi Bianchi works in Rome for Microsoft.
"""


detectors = {
    "spaCy": SpacyDetector(),
    "Hugging Face": HuggingFaceDetector(),
    "GLiNER": GlinerDetector()
}


for name, detector in detectors.items():

    print(f"\n===== {name} =====")

    results = detector.detect(text)

    for result in results:
        print(result)