import random

class MockBroker:
    def __init__(self):
        self.balance = 100000
        self.positions = []

    def place_order(self, symbol, side, quantity, price):
        trade = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "status": "filled"
        }
        if side == "buy":
            self.balance -= quantity * price
            self.positions.append(trade)
        elif side == "sell":
            self.balance += quantity * price
            self.positions = [p for p in self.positions if p['symbol'] != symbol]
        return trade

    def get_balance(self):
        return self.balance

    def get_positions(self):
        return self.positions

