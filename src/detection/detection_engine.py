from detection.regex_detector import detect_dataframe
from detection.ner_detector import detect_ner
from detection.hf_detector import detect_hf
from detection.gliner_detector import detect_gliner


NER_COLUMNS = []


def detect_all(df, detector="spacy"):

    regex_results = detect_dataframe(df)

    ner_results = []

    for column in NER_COLUMNS:

        if column not in df.columns:
            continue

        for row, value in df[column].items():

            text = str(value)

            if detector == "spacy":
                entities = detect_ner(
                    text,
                    row=row,
                    column=column
                )

            elif detector == "huggingface":
                entities = detect_hf(
                    text,
                    row=row,
                    column=column
                )

            elif detector == "gliner":
                entities = detect_gliner(
                    text,
                    row=row,
                    column=column
                )

            else:
                raise ValueError(
                    f"Unknown detector: {detector}"
                )

            ner_results.extend(entities)

    return regex_results + ner_results