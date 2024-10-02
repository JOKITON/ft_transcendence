import os
import requests

def load_key(file_path):
    with open(file_path, 'r') as key_file:
        return key_file.read()