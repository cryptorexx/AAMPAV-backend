import os
import requests
from cryptography.fernet import Fernet
from pathlib import Path
import json

BROKER_JSON_PATH = Path(__file__).resolve().parent / "brokers.json"

def encrypt_broker_credentials(key, fernet):
    with open(BROKER_JSON_PATH, "r") as file:
        brokers = json.load(file)
    for broker in brokers:
        broker["api_key"] = encrypt_data(broker["api_key"], fernet)
        broker["api_secret"] = encrypt_data(broker["api_secret"], fernet)
    with open(BROKER_JSON_PATH, "w") as file:
        json.dump(brokers, file, indent=2)

def load_key(key_path="secret.key"):
    if not os.path.exists(key_path):
        with open(key_path, "wb") as f:
            f.write(Fernet.generate_key())
    with open(key_path, "rb") as f:
        return f.read()

def auto_initialize_env_live(source_url, key_path="secret.key", env_path=".env"):
    key = load_key(key_path)
    fernet = Fernet(key)

    # Fetch live API credentials from secure remote
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        secrets = response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch broker secrets: {e}")

    # Read existing .env if exists
    existing = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as file:
            for line in file:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing[k] = v

    # Encrypt and append missing keys
    with open(env_path, "a") as file:
        for key_name, plain_value in secrets.items():
            if key_name not in existing:
                encrypted = fernet.encrypt(plain_value.encode()).decode()
                file.write(f"{key_name}={encrypted}\n")

def encrypt_string(plain_string):
    key = load_or_generate_key()
    fernet = Fernet(key)
    encrypted_string = fernet.encrypt(plain_string.encode()).decode()
    return encrypted_string

def save_to_env(encrypted_string):
    with open(".env", "w") as f:
        f.write(f"ENCRYPTED_API_KEY={encrypted_string}\n")
    print("✅ .env file created with encrypted API key.")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    generate_key()
    
    api_key = "PASTE_YOUR_REAL_API_KEY_HERE"  # Replace this with your real API key
    encrypted_api_key = encrypt_string(api_key)
    
    save_to_env(encrypted_api_key)

def load_decrypted_env_variable(env_file_path=".env"):
    key = load_or_generate_key()
    fernet = Fernet(key)

    with open(env_file_path, 'r') as env_file:
        for line in env_file:
            if line.startswith("ENCRYPTED_BROKER_API_KEY:"):
                encrypted_value = line.strip().split(":", 1)[1]
                return fernet.decrypt(encrypted_value.encode()).decode()

    raise ValueError("Encrypted API key not found in .env")

from cryptography.fernet import Fernet

def load_key(key_path="secret.key"):
    with open(key_path, "rb") as file:
        return file.read()

def decrypt_env_value(encrypted_value, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_value.encode()).decode()

def load_decrypted_credentials(env_path=".env"):
    key = load_or_generate_key()
    creds = {}
    with open(env_path, "r") as env_file:
        for line in env_file:
            if ":" in line:
                k, v = line.strip().split(":", 1)
                try:
                    creds[k] = decrypt_env_value(v, key)
                except Exception:
                    creds[k] = None
    return creds
    
KEY_FILE = "secret.key"

def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

def encrypt_data(data, key=None):
    key = key or load_or_generate_key()
    return Fernet(key).encrypt(data.encode()).decode()

def decrypt_data(token, key=None):
    key = key or load_or_generate_key()
    return Fernet(key).decrypt(token.encode()).decode()

__all__ = ['load_or_generate_key', 'encrypt_data', 'decrypt_data']
