from detection.regex_detector import detect_dataframe
from detection.ner_detector import detect_ner

NER_COLUMNS = []

def detect_all(df):
    regex_results = detect_dataframe(df)
    ner_results = []
    for column in NER_COLUMNS:
        if column not in df.columns:
            continue
        for row,value in df[column].items():
            
            entities = detect_ner(
                str(value),
                row=row,
                column=column
            )
            ner_results.extend(entities)
    return regex_results + ner_results