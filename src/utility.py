import json

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"error: file {file_path} not found.")
        exit()
    except json.JSONDecodeError:
        print(f"error: cannot decode {file_path}.")
        exit()
