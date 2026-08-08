from detection.hf_detector import detect_hf
from detection.ner_detector import detect_ner

def compare_detectors(text):
    results = {
        "spacy" : detect_ner(text),
        "huggingface" : detect_hf(text)
        }
    return results


if __name__ == "__main__":

    text = """
    Mario Rossi visited Policlinico di Messina in Italy.
    Luigi Bianchi works in Rome for Microsoft.
    """

    results = compare_detectors(text)

    print("\n===== spaCy =====")

    for entity in results["spacy"]:
        print(entity)

    print("\n===== Hugging Face =====")

    for entity in results["huggingface"]:
        print(entity)