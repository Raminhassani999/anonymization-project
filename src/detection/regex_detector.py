import pandas as pd
import re
from normalization.universal_loader import load_any_file
def detect_pii(text):
    results = {
        "emails" : [],
        "dates" : [],
        "phones" : []
    }
    results["emails"] = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" , text)
    results["dates"] = re.findall(r"\b\d{2}/\d{2}/\d{4}\b" , text)
    results["phones"] = re.findall(r"(?:\+\d{1,3}\s?)?\d{9,10}", text)
    return results

def detect_dataframe(df):
    result = []
    for column in df.columns:
        for index, value in df[column].items():
            text = str(value)
            matches = detect_pii(text)
            if any(matches.values()):
                result.append({
                    "row" : row,
                    "column" : column,
                    "value" : text,
                    "matches" : matches
                    })
    return result

if __name__ == "__main__":
    
    text = """
    Patient: Mario Rossi
    Email: mario.rossi@gmail.com
    Birth date: 15/03/1985
    Phone: +39 3331234567
    """
    
    result = detect_pii(text)
    
    print(result)