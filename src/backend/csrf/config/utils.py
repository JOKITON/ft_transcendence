import os
import requests

def fetch_key_from_service(key_type):
    url = f"http://keys:8000/api/key/{key_type}-key/"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch {key_type} key: {response.status_code} {response.text}")

def load_key(key_type):
    return fetch_key_from_service(key_type)