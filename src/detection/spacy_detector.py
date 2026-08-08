from detection.ner_detector import detect_ner
from detection.detector_interface import Detector


class SpacyDetector(Detector):

    def detect(self, text, row=None, column=None):
        return detect_ner(
            text,
            row=row,
            column=column
        )