import requests
import json
from encryption_utils import encrypt_data, load_or_generate_key, update_env_var

BROKER_JSON_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/broker_credentials.json"

def fetch_and_apply_credentials():
    key = load_or_generate_key()
    fernet_encrypt = lambda x: encrypt_data(x, key)

    try:
        response = requests.get(BROKER_JSON_URL)
        if response.status_code != 200:
            raise Exception("Failed to fetch broker credentials.")

        data = response.json()

        for broker, creds in data.items():
            for var_name, plain_val in creds.items():
                encrypted_val = fernet_encrypt(plain_val)
                update_env_var(var_name, encrypted_val)

        print("✅ Broker credentials from JSON applied and encrypted.")
    except Exception as e:
        print(f"❌ Error applying credentials: {e}")
