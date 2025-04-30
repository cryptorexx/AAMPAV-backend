import random
from .risk_controller import RiskController
from .broker_interface import MockBroker

class TradeEngine:
    def __init__(self):
        self.broker = MockBroker()
        self.risk = RiskController(self.broker)

    def decide_trade(self, signal):
        symbol = signal.get("symbol", "AAPL")
        action = signal.get("action", "buy")
        price = signal.get("price", 150)
        quantity = signal.get("quantity", 1)

        if not self.risk.check_risk(symbol, action, quantity, price):
            return {"status": "rejected", "reason": "risk_control"}

        return self.broker.place_order(symbol, action, quantity, price)

