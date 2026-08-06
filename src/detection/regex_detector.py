import pandas as pd
import re

PII_COLUMNS = {
    "Patient Code": "patient_code",
    "Tax Code": "tax_code",
    "Birth Date": "date",
    "Assessment Date": "date",
    "Age At Assessment" : "age"
}

def detect_email(text):
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

def detect_date(text):
    return re.findall(r"\b(\d{2}/\d{2}/\d{2}|\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})\b" , text)

def detect_phones(text):
    return re.findall(r"(?:\+\d{1,3}\s?)?\d{9,10}" , text)

def detect_patient_code(text):
    return re.findall(r"\b[A-Z]\d{5}\b", text)

def detect_tax_code(text):
    return re.findall(r"\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b" , text)


def detect_pii(text):
    results = {
        "emails" : detect_email(text),
        "dates" : detect_date(text),
        "phones" : detect_phones(text),
        "patient_codes" : detect_patient_code(text),
        "tax_code" : detect_tax_code(text)
    }
    
    return results

def detect_dataframe(df):
    result = []
    for column in df.columns:
        if column not in PII_COLUMNS:
            continue
        for index, value in df[column].items():
            text = str(value)
            matches = {}
            if PII_COLUMNS[column] == "patient_code":
                matches["patient_codes"] = detect_patient_code(text)
            elif PII_COLUMNS[column] == "tax_code":
                matches['tax_codes'] = detect_tax_code(text)
            elif PII_COLUMNS[column] == "date":
                matches["dates"] = detect_date(text)
            elif PII_COLUMNS[column] == "age":
                matches["age"] = [text]
            if any(matches.values()):
                result.append({
                    "row" : index,
                    "column" : column,
                    "value" : text,
                    "matches" : matches
                    })
    return result