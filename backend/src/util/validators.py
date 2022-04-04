import os
import json

validators = {}

# obtain a validator object of a specific name
def get(collection_name: str):
    if collection_name not in validators:
        with open(f'./src/static/validators/{collection_name}.json', 'r') as f:
            validators[collection_name] = json.load(f)
    return validators[collection_name]