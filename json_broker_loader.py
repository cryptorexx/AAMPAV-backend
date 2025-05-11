import json
import requests
from encryption_utils import encrypt_data, load_or_generate_key, update_env_var

BROKER_JSON_URL = "https://raw.githubusercontent.com/cryptorexx/broker-secrets/main/broker_credentials.json"

def fetch_and_apply_credentials():
    key = load_or_generate_key()
    fernet_encrypt = lambda x: encrypt_data(x, key)

    try:
        response = requests.get(BROKER_JSON_URL)
        response.raise_for_status()
        data = response.json()

        for broker, creds in data.items():
            for var, value in creds.items():
                if value:
                    encrypted = fernet_encrypt(value)
                    update_env_var(var, encrypted)

        print("✅ Broker credentials encrypted and loaded into .env.")
    except Exception as e:
        print(f"❌ Error loading broker credentials: {e}")
