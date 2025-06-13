import json
import os

DATABASE_FILE = "data/characters_male.json"

def load_data():
    """Load character data from JSON file"""
    try:
        # Create src directory if it doesn't exist
        os.makedirs("src", exist_ok=True)
        
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error loading database, starting with empty database")
        return []

def save_data(characters):
    """Save character data to JSON file"""
    try:
        # Create src directory if it doesn't exist
        os.makedirs("src", exist_ok=True)
        
        with open(DATABASE_FILE, 'w', encoding='utf-8') as file:
            json.dump(characters, file, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving database: {e}")
        return False

def add_character(characters, character_data):
    """Add a new character to the database"""
    characters.append(character_data)
    return save_data(characters)

def search_characters(characters, **filters):
    """Search characters by attributes"""
    results = characters
    for key, value in filters.items():
        results = [char for char in results if char.get(key, "").lower() == str(value).lower()]
    return results