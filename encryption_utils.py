import os
import json
import requests
from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = "secret.key"
ENV_PATH = ".env"
BROKER_JSON_PATH = Path(__file__).resolve().parent / "brokers.json"


# ========================== CORE KEY MANAGEMENT ==========================

def load_or_generate_key(key_path=KEY_FILE):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(key)
        return key


# ========================== ENCRYPT / DECRYPT ==========================

def encrypt_data(data, key=None):
    key = key or load_or_generate_key()
    return Fernet(key).encrypt(data.encode()).decode()

def decrypt_data(token, key=None):
    key = key or load_or_generate_key()
    return Fernet(key).decrypt(token.encode()).decode()


# ========================== ENV VAR HANDLING ==========================

def update_env_var(var_name, encrypted_value, env_path=ENV_PATH):
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

def get_or_encrypt_env_var(var_name, plain_value=None, key_path=KEY_FILE, env_path=ENV_PATH):
    key = load_or_generate_key(key_path)
    fernet = Fernet(key)

    current = os.getenv(var_name)
    if current and not current.startswith("gAAAA"):
        encrypted = fernet.encrypt(current.encode()).decode()
        update_env_var(var_name, encrypted, env_path)
        return current
    elif current and current.startswith("gAAAA"):
        return fernet.decrypt(current.encode()).decode()
    elif plain_value:
        encrypted = fernet.encrypt(plain_value.encode()).decode()
        update_env_var(var_name, encrypted, env_path)
        return plain_value
    else:
        raise Exception(f"{var_name} is not set and no fallback provided.")


# ========================== .env UTILITIES ==========================

def load_decrypted_credentials(env_path=ENV_PATH):
    key = load_or_generate_key()
    fernet = Fernet(key)
    creds = {}

    with open(env_path, "r") as env_file:
        for line in env_file:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                try:
                    creds[k] = fernet.decrypt(v.encode()).decode()
                except Exception:
                    creds[k] = None
    return creds


# ========================== BROKER JSON ENCRYPTION ==========================

def encrypt_broker_credentials(key=None):
    key = key or load_or_generate_key()
    fernet = Fernet(key)

    with open(BROKER_JSON_PATH, "r") as file:
        brokers = json.load(file)

    for broker in brokers:
        broker["api_key"] = encrypt_data(broker["api_key"], key)
        broker["api_secret"] = encrypt_data(broker["api_secret"], key)

    with open(BROKER_JSON_PATH, "w") as file:
        json.dump(brokers, file, indent=2)


# ========================== REMOTE INIT ==========================

def auto_initialize_env_live(source_url, key_path=KEY_FILE, env_path=ENV_PATH):
    key = load_or_generate_key(key_path)
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


# ========================== STRING UTILS ==========================

def encrypt_string(plain_string):
    return encrypt_data(plain_string)

def save_to_env(encrypted_string, var_name="ENCRYPTED_API_KEY"):
    with open(ENV_PATH, "w") as f:
        f.write(f"{var_name}={encrypted_string}\n")
    print(f"✅ .env file created with encrypted {var_name}.")


# ========================== MAIN EXECUTION FOR QUICK ENCRYPT ==========================

if __name__ == "__main__":
    # You can call this directly to encrypt and store a single key
    api_key = "PASTE_YOUR_REAL_API_KEY_HERE"
    encrypted_api_key = encrypt_string(api_key)
    save_to_env(encrypted_api_key)
