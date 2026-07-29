import pandas as pd

def load_json(file_path):
    data = pd.read_json(file_path)
    return data

if __name__ == "__main__":
    
    file_path = "data/sample_data/sample.json"
    
    df = load_json(file_path)
    
    print(df.head())
    print("\nDataset shape:")
    print(df.shape)