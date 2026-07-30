from excel_loader import load_excel

def create_common_format(content , source_type , data_type):
    common_data = {
        "source" : source_type,
        "type" : data_type,
        "content" : content
    }
    return common_data

if __name__ == "__main__":
    
    file_path = "../../data/diabetology/diabetology-synthetic-dataset.xlsx"
    
    df = load_excel(file_path)
    
    result = create_common_format(
        df,
        "excel",
        "structured"
    )

    print(result["source"])
    print(result["type"])
    print("\nDataset preview:")
    print(result["content"].head())
    print("\nDataset shape:")
    print(result["content"].shape)