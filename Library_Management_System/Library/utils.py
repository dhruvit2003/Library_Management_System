import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), 'library_data.json')

def read_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
