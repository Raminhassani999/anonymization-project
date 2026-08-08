from detection.ner_detector import detect_ner
from detection.detector_interface import Detector


class SpacyDetector(Detector):

    def detect(self, text, row=None, column=None):
        results = detect_ner(
            text,
            row=row,
            column=column
        )
        for result in results:
            value = result["value"]

            start = text.find(value)

            if start != -1:
                result["start"] = start
                result["end"] = start + len(value)

        return results