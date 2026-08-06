def redact_patient_code(value):
    return "[PATIENT_CODE]"


def redact_tax_code(value):
    return "[TAX_CODE]"


def redact_date(value):
    return "[DATE]"


def mask_patient_code(value):
    return value[:2] + "*" * (len(value) - 2)

def mask_tax_code(value):
    return value[:3] + "*" * (len(value) - 5) + value[-2:]

def mask_date(value):
    if "/" in value:
        return "**/**/" + value[-2:]
    elif "-" in value:
        return value[:4] + "-**-**"
    return value


def anonymize_dataframe(df , detections , method="redact"):
    anonymised_df = df.copy()
    for item in detections:
        row = item["row"]
        column = item["column"]
        
        if column == "Patient Code":
            if method == "redact":
                anonymised_df.at[row, column] = redact_patient_code(
                    anonymised_df.at[row, column])
            elif method == "mask":
                        anonymised_df.at[row, column] = mask_patient_code(
                            anonymised_df.at[row, column]
                    )    
                
                
                
        elif column == "Tax Code":
            if method == "redact":
                anonymised_df.at[row, column] = redact_tax_code(
                    anonymised_df.at[row, column])
            elif method == 'mask':
                anonymised_df.at[row , column] = mask_tax_code(
                    anonymised_df.at[row , column]
                    )
            
            
            
        elif column in ["Birth Date", "Assessment Date"]:
            if method == "redact":
                anonymized_df.at[row, column] = redact_date(
                    anonymized_df.at[row, column])
            elif method == "mask":
                anonymised_df.at[row , column] = mask_date(
                    anonymised_df.at[row , column]
                    )
    return anonymised_df