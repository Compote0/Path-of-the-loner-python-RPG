import json

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        exit()
    except json.JSONDecodeError:
        print(f"Erreur : Impossible de lire le fichier {file_path}.")
        exit()
