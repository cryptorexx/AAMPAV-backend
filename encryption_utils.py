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
    
    api_key = "test-abc123456789"  # Replace this with your real API key
    encrypted_api_key = encrypt_string(api_key)
    
    save_to_env(encrypted_api_key)
