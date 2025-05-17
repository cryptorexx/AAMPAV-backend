import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from execution_ai.brokers.alpaca_broker import AlpacaBroker
from execution_ai.brokers.base_broker import BaseBroker
from execution_ai.brokers.auto_broker_handler import AutoBrokerHandler
from execution_ai.brokers.broker_utils import load_brokers, save_brokers
from encryption_utils import load_or_generate_key, encrypt_data, decrypt_data
from config import USE_SIMULATED_BROKER

load_dotenv()

class BrokerInterface:
    def __init__(self):
        if USE_SIMULATED_BROKER:
            self.selected_broker = "SimulatedBroker"
            self.api_key = "SIMULATED"
        else:
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
            print(f"[REAL] Executing {side.upper()} order via broker")
            return {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "submitted",
                "broker": self.selected_broker
            }
