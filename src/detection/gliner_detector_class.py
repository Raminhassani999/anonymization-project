from detection.gliner_detector import detect_gliner
from detection.detector_interface import Detector


class GlinerDetector(Detector):

    def detect(self, text, row=None, column=None):
        return detect_gliner(
            text,
            row=row,
            column=column
        )