import pandas as pd

def load_excel(file_path):
    data = pd.read_excel(file_path)
    return data

if __name__ == "__main__":
    
    file_path = "data/diabetology/diabetology-synthetic-dataset.xlsx"
    
    df = load_excel(file_path)
    print(df.head())
    print("\nDataset shape:")
    print(df.shape)