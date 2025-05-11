import os
import json
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from execution_ai.brokers.alpaca_broker import AlpacaBroker
from execution_ai.brokers.base_broker import BaseBroker
from execution_ai.brokers.auto_broker_handler import AutoBrokerHandler
from encryption_utils import load_or_generate_key, encrypt_data, decrypt_data
load_dotenv()  # Load from .env
from config import USE_SIMULATED_BROKER
from execution_ai.brokers.auto_broker_handler import AutoBrokerHandler
from pathlib import Path

BROKER_JSON_PATH = Path(__file__).resolve().parent.parent / "brokers.json"

def load_brokers():
    if BROKER_JSON_PATH.exists():
        with open(BROKER_JSON_PATH, "r") as file:
            return json.load(file)
    return []

def save_brokers(brokers):
    with open(BROKER_JSON_PATH, "w") as file:
        json.dump(brokers, file, indent=2)

def load_brokers(file_path="config/brokers.json"):
    with open(file_path, "r") as f:
        return json.load(f)

class BrokerInterface:
    def __init__(self):
        self.handler = AutoBrokerHandler()
        result = self.handler.scan_and_select()
        self.broker_name = result["selected"]
        self.broker_instance = result["instance"]

    def place_order(self, symbol, qty, side):
        if not self.broker_instance:
            return {"error": "No available broker"}
        return self.broker_instance.place_order(symbol, qty, side)

class BrokerInterface:
    def __init__(self):
        if USE_SIMULATED_BROKER:
            self.selected_broker = "SimulatedBroker"
            self.api_key = "SIMULATED"
        else:
            # Your real broker logic (commented or included here)
            from execution_ai.brokers.auto_broker_handler import AutoBrokerHandler
            handler = AutoBrokerHandler()
            self.api_key = handler.register_with_broker()["api_key"]
            self.selected_broker = handler.scan_and_select()["selected"]

    def place_order(self, symbol, qty, side, type="market", time_in_force="gtc"):
        if USE_SIMULATED_BROKER:
            print(f"[SIMULATED] {side.upper()} {qty} {symbol}")
            return {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "filled",
                "broker": "simulated"
            }
        else:
            # Real broker execution (can be a call to Alpaca, etc.)
            print(f"[REAL] Executing {side.upper()} order via broker")
            return {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "submitted",
                "broker": self.selected_broker
            }

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
