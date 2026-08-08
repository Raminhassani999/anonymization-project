from transformers import pipeline


MODEL_NAME = "Davlan/xlm-roberta-base-ner-hrl"

ner_pipeline = None


def detect_hf(text, row=None, column=None):
    global ner_pipeline

    if ner_pipeline is None:
        ner_pipeline = pipeline(
            "ner",
            model=MODEL_NAME,
            aggregation_strategy="simple"
        )
    results = ner_pipeline(text)

    entities = []

    for entity in results:
        entities.append({
            "row": row,
            "column": column,
            "value": entity["word"],
            "entity": entity["entity_group"],
            "start": entity["start"],
            "end": entity["end"],
            "score": float(entity["score"]),
            "source": "huggingface"
        })

    return entities


if __name__ == "__main__":

    text = """
    Mario Rossi visited Policlinico di Messina in Italy.
    """

    results = detect_hf(text)

    for result in results:
        print(result)