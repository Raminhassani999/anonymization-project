from detection.hf_detector import detect_hf
from detection.detector_interface import Detector


class HuggingFaceDetector(Detector):

    def detect(self, text, row=None, column=None):
        return detect_hf(
            text,
            row=row,
            column=column
        )