import os
import json
import requests
from pathlib import Path
from cryptography.fernet import Fernet

# === CONFIG ===
KEY_FILE = "secret.key"
ENV_PATH = ".env"
BROKER_JSON_PATH = Path(__file__).resolve().parent / "brokers.json"


# === KEY HANDLING ===
def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key


# === BASIC ENCRYPT / DECRYPT ===
def encrypt_data(data, key=None):
    key = key or load_or_generate_key()
    return Fernet(key).encrypt(data.encode()).decode()

def decrypt_data(token, key=None):
    key = key or load_or_generate_key()
    return Fernet(key).decrypt(token.encode()).decode()


# === ENV MANAGEMENT ===
def update_env_var(var_name: str, encrypted_value: str, env_path: str = ENV_PATH):
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith(f"{var_name}="):
                    lines.append(f"{var_name}={encrypted_value}\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{var_name}={encrypted_value}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)


def get_or_encrypt_env_var(var_name: str, plain_value: str = None):
    key = load_or_generate_key()
    fernet = Fernet(key)
    current = os.getenv(var_name)

    if current and not current.startswith("gAAAA"):
        encrypted = fernet.encrypt(current.encode()).decode()
        update_env_var(var_name, encrypted)
        return current
    elif current and current.startswith("gAAAA"):
        return fernet.decrypt(current.encode()).decode()
    elif plain_value:
        encrypted = fernet.encrypt(plain_value.encode()).decode()
        update_env_var(var_name, encrypted)
        return plain_value
    else:
        raise ValueError(f"{var_name} is not set and no fallback provided.")


def load_decrypted_env_variable(var_name="ENCRYPTED_API_KEY", env_path=ENV_PATH):
    key = load_or_generate_key()

    if not os.path.exists(env_path):
        raise FileNotFoundError(".env file is missing")

    with open(env_path, "r") as file:
        for line in file:
            if line.startswith(f"{var_name}="):
                encrypted_value = line.strip().split("=", 1)[1]
                return Fernet(key).decrypt(encrypted_value.encode()).decode()

    raise ValueError(f"{var_name} not found in .env")


# === CREDENTIAL ENCRYPTION FOR BROKERS.JSON ===
def encrypt_broker_credentials():
    key = load_or_generate_key()
    with open(BROKER_JSON_PATH, "r") as file:
        brokers = json.load(file)

    for broker in brokers:
        broker["api_key"] = encrypt_data(broker["api_key"], key)
        broker["api_secret"] = encrypt_data(broker["api_secret"], key)

    with open(BROKER_JSON_PATH, "w") as file:
        json.dump(brokers, file, indent=2)


# === AUTO INITIALIZER FROM REMOTE ===
def auto_initialize_env_live(source_url, env_path=ENV_PATH):
    key = load_or_generate_key()
    fernet = Fernet(key)

    try:
        response = requests.get(source_url)
        response.raise_for_status()
        secrets = response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch broker secrets: {e}")

    existing = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as file:
            for line in file:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing[k] = v

    with open(env_path, "a") as file:
        for key_name, plain_value in secrets.items():
            if key_name not in existing:
                encrypted = fernet.encrypt(plain_value.encode()).decode()
                file.write(f"{key_name}={encrypted}\n")


# === DEV TOOL TO GENERATE ENV FILE FROM STRING ===
def save_to_env(plain_api_key):
    encrypted = encrypt_data(plain_api_key)
    update_env_var("ENCRYPTED_API_KEY", encrypted)
    print("✅ .env file created with encrypted API key.")


# === OPTIONAL MAIN ===
if __name__ == "__main__":
    # Only for manual setup/testing. Not needed in production
    api_key = "PASTE_YOUR_REAL_API_KEY_HERE"
    save_to_env(api_key)
