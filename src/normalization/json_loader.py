import pandas as pd
def load_json(file_path):
    data = pd.read_json(file_path)
    return data