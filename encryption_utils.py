from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

def generate_key():
    # Generate a new encryption key and save it
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key saved to secret.key")

def encrypt_string(plain_string):
    # Load the encryption key
    with open("secret.key", "rb") as key_file:
        key = key_file.read()
    fernet = Fernet(key)
    
    # Encrypt the given string
    encrypted_string = fernet.encrypt(plain_string.encode()).decode()
    return encrypted_string

def save_to_env(encrypted_string):
    # Save the encrypted string to a .env file
    with open(".env", "w") as f:
        f.write(f"ENCRYPTED_API_KEY={encrypted_string}")
    print(".env file created with encrypted API key.")

# Step 1: Generate a new key
generate_key()

# Step 2: Encrypt your API key
api_key = "PASTE_YOUR_REAL_API_KEY_HERE"  # Replace with your real API key
encrypted_api_key = encrypt_string(api_key)

# Step 3: Save the encrypted API key to .env
save_to_env(encrypted_api_key)

