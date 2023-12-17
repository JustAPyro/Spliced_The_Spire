# importing the module
import json

from new.abstractions import AbstractEnemy
import csv

from tests.BugTracker import BugTracker, BugType, BugArea

implemented_enemies = [sc.__name__ for sc in AbstractEnemy.__subclasses__()]


# Opening JSON file
with open('test_data.json') as json_file:
    data = json.load(json_file)
    for enemy in data['start']:
        name: str = enemy['name']
        name.replace(' ', '')
        name.replace(')', '')
        name.replace('(', '')
        if name not in implemented_enemies:
            print(f'WARNING: Could not find enemy implementation for: {name}')
            BugTracker('bd.db').file(BugType.UNIMPLEMENTED, BugArea.MONSTER, name)
