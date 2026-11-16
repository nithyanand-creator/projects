from pathlib import Path
import json
BASE = Path(__file__).parent

def load(name):
    with open(BASE/ (name + ".json"), encoding="utf-8") as f:
        return json.load(f)

def save(name, items):
    with open(BASE/ (name + ".json"), "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)