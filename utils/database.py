import json

def load_data(file_path):
    """
    Charge un fichier JSON et renvoie son contenu.
    
    Args:
        file_path (str): Chemin du fichier JSON.
    
    Returns:
        dict: Contenu du fichier JSON.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON - {file_path}")
        return {}
