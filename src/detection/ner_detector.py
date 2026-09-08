import spacy
nlp_en = spacy.load("en_core_web_sm")
nlp_it = spacy.load("it_core_news_sm")

def detect_ner(text , row=None , column=None):
    doc_en = nlp_en(text)
    doc_it = nlp_it(text)
    entities = []
    for doc in [doc_en , doc_it]:
        for ent in doc.ents:
            
            entities.append({
                "row" : row,
                "column" : column,
                "value": ent.text,
                "entity": ent.label_,
                "source" : "ner",
                "start": ent.start_char,
                "end": ent.end_char
            })
    
    unique_entities = {}

    for entity in entities:
        key = (entity["start"], entity["end"])

        if key not in unique_entities:
            unique_entities[key] = entity

    return list(unique_entities.values())