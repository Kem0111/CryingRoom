import json


def read_messages(path):
    with open(path, 'r') as f:
        content = f.read()
        text = json.loads(content)
    return text
