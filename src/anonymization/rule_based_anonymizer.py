def anonymize_dataframe(df , detections):
    anonymised_df = df.copy()

    for item in detections:
        row = item["row"]
        column = item["column"]
        
        if column == "Patient Code":
            anonymised_df.at[row , column] = "[PATIENT_CODE]"
        elif column == "Tax Code":
            anonymised_df.at[row , column] = "[TAX_CODE]"
        elif column in ["Birth Date", "Assessment Date"]:
            anonymised_df.at[row , column] = "[DATE]"
    return anonymised_df