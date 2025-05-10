import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from execution_ai.brokers.alpaca_broker import AlpacaBroker
from execution_ai.brokers.base_broker import BaseBroker
from execution_ai.brokers.auto_broker_handler import AutoBrokerHandler
from encryption_utils import load_or_generate_key, encrypt_data, decrypt_data
load_dotenv()  # Load from .env

class BrokerInterface:
    def __init__(self):
        self.handler = AutoBrokerHandler()
        result = self.handler.scan_and_select()
        self.api_key = self.handler.register_with_broker()["api_key"]
        self.selected_broker = result["selected"]
        
    def place_order(self, symbol, qty, side, type="market", time_in_force="gtc"):
        print(f"[AUTO-BROKER] Placing {side.upper()} order for {qty} {symbol} (simulated)")
        return {
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "status": "filled",
            "broker": "auto-placeholder"
        }

# Load encryption key
key = load_or_generate_key()
fernet = Fernet(key)

def get_or_encrypt_env_var(var_name: str, plain_value: str = None):
    """
    Check if an env var is encrypted. If not, encrypt and update .env.
    """
    current = os.getenv(var_name)
    if current and not current.startswith("gAAAA"):
        # Value exists but not encrypted
        encrypted = encrypt_data(current, fernet)
        update_env_var(var_name, encrypted)
        return current
    elif current and current.startswith("gAAAA"):
        return decrypt_data(current, fernet)
    elif plain_value:
        encrypted = encrypt_data(plain_value, fernet)
        update_env_var(var_name, encrypted)
        return plain_value
    else:
        raise Exception(f"{var_name} not set and no fallback provided.")

def update_env_var(var_name, value):
    """
    Update the .env file with a new encrypted value.
    """
    from pathlib import Path
    env_path = Path(".env")
    lines = []
    found = False
    if env_path.exists():
        with env_path.open("r") as file:
            for line in file:
                if line.startswith(f"{var_name}="):
                    lines.append(f"{var_name}={value}\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{var_name}={value}\n")

    with env_path.open("w") as file:
        file.writelines(lines)

class BrokerFactory:
    """
    Returns an instance of a broker based on type.
    """
    @staticmethod
    def get_broker(broker_name: str) -> BaseBroker:
        if broker_name.lower() == "alpaca":
            api_key = get_or_encrypt_env_var("ALPACA_API_KEY")
            api_secret = get_or_encrypt_env_var("ALPACA_API_SECRET")
            return AlpacaBroker(api_key, api_secret)
        else:
            raise ValueError(f"Unsupported broker: {broker_name}")
