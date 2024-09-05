import os

def load_key(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"The file {filename} does not exist.")
    
    with open(filename, 'r') as key_file:
        key_content = key_file.read()

    return key_content