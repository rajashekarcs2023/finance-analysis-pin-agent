import json
import os

def ensure_directory(directory_path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path (str): Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        
def save_json(data, file_path):
    """
    Save data as JSON to the specified path.
    
    Args:
        data (dict): Data to save
        file_path (str): Path to save the JSON file
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
        
def load_json(file_path):
    """
    Load JSON data from the specified path.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        dict: Loaded JSON data
    """
    with open(file_path, 'r') as f:
        return json.load(f) 