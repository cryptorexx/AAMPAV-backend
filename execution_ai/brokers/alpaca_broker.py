import os
import requests
from execution_ai.brokers.base_broker import BaseBroker

class AlpacaBroker(BaseBroker):
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.base_url = "https://paper-api.alpaca.markets"
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }

    def connect(self):
        url = f"{self.base_url}/v2/account"
        response = requests.get(url, headers=self.headers)
        return response.ok

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
        if response.status_code in (200, 201):
            return response.json()
        return {"error": response.text}

    def get_account_info(self):
        url = f"{self.base_url}/v2/account"
        response = requests.get(url, headers=self.headers)
        return response.json()
