# execution_ai/broker_interface.py
import os
import requests

class AlpacaBroker:
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        self.base_url = "https://paper-api.alpaca.markets"
        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
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
        return {"error": response.text}
