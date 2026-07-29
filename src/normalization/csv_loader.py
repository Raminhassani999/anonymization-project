import pandas as pd

def load_csv(file_path):
    
    data = pd.read_csv(file_path)
    
    return data

if __name__ == "__main__":
    
    file_path = "data/sample_data/sample.csv"
    
    df = load_csv(file_path)
    
    print(df.head())
    print("\nDataset shape:")
    print(df.shape)