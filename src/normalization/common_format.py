def create_common_format(content , source_type , data_type):
    common_data = {
        "source" : source_type,
        "type" : data_type,
        "content" : content
    }
    return common_data

if __name__ == "__main__":
    
    example_data = {
        "Name": "Mario Rossi",
        "Birth Date": "15/03/1985"
    }
    
    result = create_common_format(
        example_data,
        "excel",
        "structured"
    )

    print(result)