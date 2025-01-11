import json


def print_json(what_to_print: dict):
    print()
    print(json.dumps(what_to_print, indent=4, sort_keys=True))
    print()
