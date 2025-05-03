from cryptography.fernet import Fernet
import os

# Generate a new Fernet key (only once, store it securely)
def generate_key():
    return Fernet.generate_key()

# Save the key to a file (do only once)
def save_key(key: bytes, filename="secret.key"):
    with open(filename, "wb") as key_file:
        key_file.write(key)

# Load the key
def load_key(filename="secret.key"):
    return open(filename, "rb").read()

# Encrypt sensitive data
def encrypt_message(message: str, key: bytes) -> str:
    return Fernet(key).encrypt(message.encode()).decode()

# Decrypt encrypted data
def decrypt_message(token: str, key: bytes) -> str:
    return Fernet(key).decrypt(token.encode()).decode()
