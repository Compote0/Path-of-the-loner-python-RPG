import json
from src.utility import load_data

def create_main_character(character_data):
    """
    Creates a JSON object representing the main character based on the selected class data.
    """
    # Load JSON files for spells, weapons, and ancestry
    spells = load_data("data/spells.json")
    weapons = load_data("data/weapons.json")
    ancestry = load_data("data/ancestry.json")

    # Filter spells, weapons, and ancestry compatible with this class
    class_spells = [spell for spell in spells if spell["class"] == character_data["class"]]
    class_weapons = [weapon for weapon in weapons if weapon["class"] == character_data["class"]]
    compatible_ancestry = [asc for asc in ancestry if character_data["class"] in asc["compatible_classes"]]

    # Create the JSON object for the main character
    main_character = {
        "name": "Hero",  # Default name
        "class": character_data["class"],
        "hp": character_data["hp"],
        "attack": character_data["attack"],
        "defense": character_data["defense"],
        "speed": character_data["speed"],
        "status": None,
        "spells": class_spells,
        "weapons": class_weapons,
        "ancestry": compatible_ancestry,
        "background": character_data.get("background", None),  # Include the background
        "image": character_data["image"]
    }

    return main_character

def save_main_character(main_character, filepath="data/main_character.json"):
    """
    Saves the main character to a JSON file.
    """
    with open(filepath, "w") as file:
        json.dump(main_character, file, indent=4)
    print(f"Main character saved to {filepath}.")

def load_main_character(filepath="data/main_character.json"):
    """
    Loads the main character from a JSON file.
    
    Args:
        filepath: Path to the JSON file.
        
    Returns:
        dict or None: The main character data, or None if the file does not exist.
    """
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No file found at {filepath}.")
        return None
