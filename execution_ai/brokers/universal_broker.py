import os
from encryption_utils import get_or_encrypt_env_var

class UniversalBroker:
    def __init__(self, broker_name: str):
        self.name = broker_name.lower()
        self.api_key = get_or_encrypt_env_var(f"{self.name.upper()}_API_KEY")
        self.secret_key = get_or_encrypt_env_var(f"{self.name.upper()}_API_SECRET", "")
        self.connected = self.connect()

    def connect(self):
        if self.api_key and (self.secret_key or self.name == "fxcm"):
            print(f"[UniversalBroker] Connected to {self.name.capitalize()} broker.")
            return True
        return False

    def place_order(self, symbol, qty, side):
        if not self.connected:
            return {"error": f"{self.name.capitalize()} not connected"}
        # Simulated order
        return {
            "broker": self.name,
            "symbol": symbol,
            "side": side,
            "qty": qty,
            "status": "filled"
        }
