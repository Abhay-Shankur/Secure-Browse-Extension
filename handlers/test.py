import json

with open('create_did.json', 'r') as file:
    didDoc = json.load(file)

print(didDoc)