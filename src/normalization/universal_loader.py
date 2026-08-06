import os
from .csv_loader import load_csv
from .json_loader import load_json
from .txt_loader import load_txt
from .excel_loader import load_excel
from .common_format import create_common_format

def load_any_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    
    if extension == ".xlsx":
        data = load_excel(file_path)
        return create_common_format(
            data,
            "excel",
            "structured"
        )
    elif extension == ".csv":
        data = load_csv(file_path)
        return create_common_format(
            data,
            "csv",
            "structured"
        )
    elif extension == ".txt":
        data = load_txt(file_path)
        return create_common_format(
            data,
            "txt",
            "text"
        )
    elif extension == ".json":
        data = load_json(file_path)
        return create_common_format(
            data,
            "json",
            "structured"
        )
    else:
        raise ValueError ("Unsupported type file")