from gliner import GLiNER


MODEL_NAME = "gliner-community/gliner_small-v2.5"

model = None


def detect_gliner(text, row=None, column=None):

    global model

    if model is None:
        model = GLiNER.from_pretrained(MODEL_NAME)

    labels = [
        "person",
        "organization",
        "location",
        "date"
    ]

    results = model.predict_entities(
        text,
        labels,
        threshold=0.5
    )

    entities = []

    for entity in results:
        entities.append({
            "row": None,
            "column": None,
            "value": entity["text"],
            "entity": entity["label"],
            "score": entity["score"],
            "start": entity["start"],
            "end": entity["end"],
            "source": "gliner"
        })

    return entities


if __name__ == "__main__":

    text = """
    Mario Rossi visited Policlinico di Messina in Italy.
    Luigi Bianchi works in Rome for Microsoft.
    """

    results = detect_gliner(text)

    for result in results:
        print(result)