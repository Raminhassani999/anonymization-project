ANONYMIZATION_POLICY = {
    "Patient Code" : "pseudonym",
    "Tax Code" : "mask",
    "Birth Date" : "generalize",
    "Assessment Date" : "generalize",
    "Age At Assessment" : "generalize"
    }

patient_map = {}
patient_counter = 1

def pseudonymize_patient_code(value):
    global patient_counter
    if value not in patient_map:
        patient_map[value] = f"PATIENT_{patient_counter:04d}"
        patient_counter += 1
    return patient_map[value]


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

def generalize_date(value):
    value = str(value)
    
    if "/" in value:
        parts = value.split("/")
        return parts[-1]

    elif "-" in value:
        parts = value.split("-")
        return parts[0]

    return value

def generalize_age(value):
    try:
        age = float(value)

        lower = int(age // 10) * 10
        upper = int(lower + 9)

        return f"{lower}-{upper}"

    except:
        return value

def anonymize_dataframe(df , detections):
    anonymised_df = df.copy().astype(str)
    for item in detections:
        row = item["row"]
        column = item["column"]
        method = ANONYMIZATION_POLICY.get(column)
        
        if column == "Patient Code":
            if method == "redact":
                anonymised_df.at[row, column] = redact_patient_code(
                    anonymised_df.at[row, column])
            elif method == "mask":
                        anonymised_df.at[row, column] = mask_patient_code(
                            anonymised_df.at[row, column]
                    )
            elif method == "pseudonym":
                anonymised_df.at[row , column] = pseudonymize_patient_code(
                    anonymised_df.at[row , column]
                )  
                
                
                
        elif column == "Tax Code":
            if method == "redact":
                anonymised_df.at[row, column] = redact_tax_code(
                    anonymised_df.at[row, column])
            elif method == 'mask':
                anonymised_df.at[row , column] = mask_tax_code(
                    anonymised_df.at[row , column]
                    )
        elif column == "Age At Assessment":
            if method == "generalize":
                anonymised_df.at[row , column] = generalize_age(
                    anonymised_df.at[row , column]
                    )
        
        elif column in ["Birth Date", "Assessment Date"]:
            if method == "redact":
                anonymised_df.at[row, column] = redact_date(
                    anonymised_df.at[row, column])
            elif method == "mask":
                anonymised_df.at[row , column] = mask_date(
                    anonymised_df.at[row , column]
                    )
            elif method == "generalize":
                anonymised_df.at[row , column] = generalize_date(
                    anonymised_df.at[row , column]
                    )
                
    return anonymised_df