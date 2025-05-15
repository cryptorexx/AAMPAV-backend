import json
from pathlib import Path

BROKER_JSON_PATH = Path(__file__).resolve().parent / "brokers.json"

def load_brokers():
    with open(BROKER_JSON_PATH, "r") as f:
        return json.load(f)

def save_brokers(data):
    with open(BROKER_JSON_PATH, "w") as f:
        json.dump(data, f, indent=2)
