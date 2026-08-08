from detection.detector_interface import Detector
from detection.hf_detector import detect_hf


class HuggingFaceDetector(Detector):

    def detect(self, text, row=None, column=None):

        results = detect_hf(text)

        for result in results:

            result["row"] = row
            result["column"] = column

        return results