import pandas as pd

def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text

if __name__ == "__main__":
    
    file_path = "data/sample_data/sample.txt"
    
    df = load_txt(file_path)
    
    print(df)