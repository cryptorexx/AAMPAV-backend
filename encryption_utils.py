from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("✅ secret.key file created.")

def encrypt_string(plain_string):
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
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

def load_decrypted_env_variable(env_file_path=".env", key_file_path="secret.key"):
    from cryptography.fernet import Fernet

    # Load secret key
    with open(key_file_path, 'rb') as key_file:
        secret_key = key_file.read()

    fernet = Fernet(secret_key)

    # Read encrypted variable
    with open(env_file_path, 'r') as env_file:
        for line in env_file:
            if line.startswith("ENCRYPTED_BROKER_API_KEY:"):
                encrypted_value = line.strip().split(":", 1)[1]
                decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
                return decrypted_value

    raise ValueError("Encrypted API key not found in .env")

from cryptography.fernet import Fernet

def load_key(key_path="secret.key"):
    with open(key_path, "rb") as file:
        return file.read()

def decrypt_env_value(encrypted_value, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_value.encode()).decode()

def load_decrypted_credentials(env_path=".env", key_path="secret.key"):
    key = load_key(key_path)
    creds = {}
    with open(env_path, "r") as env_file:
        for line in env_file:
            if ":" in line:
                k, v = line.strip().split(":", 1)
                try:
                    creds[k] = decrypt_env_value(v, key)
                except Exception:
                    creds[k] = None  # Skip malformed lines
    return creds
    
def load_or_generate_key():
    # your key loading/generation logic here
    pass

__all__ = ['load_or_generate_key', 'encrypt_data', 'decrypt_data']
