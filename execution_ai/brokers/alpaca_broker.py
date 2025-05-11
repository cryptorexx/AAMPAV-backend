# execution_ai/brokers/alpaca_broker.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AlpacaBroker:
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY", "demo")
        self.api_secret = os.getenv("ALPACA_API_SECRET", "demo")
        self.base_url = "https://paper-api.alpaca.markets"
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret
        }

    def place_order(self, symbol, qty, side, type="market", time_in_force="gtc"):
        url = f"{self.base_url}/v2/orders"
        order_data = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force
        }
        response = requests.post(url, json=order_data, headers=self.headers)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {"error": response.text}

    def ping(self):
        """Check if broker API is reachable."""
        try:
            url = f"{self.base_url}/v2/account"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except Exception:
            return False
