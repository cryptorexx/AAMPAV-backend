from portfolio_ai.portfolio_manager
import PortfolioManager

class TradeEngine:
    def __init__(self):
        self.balance = 100000  # USD
        self.trades = []

    def execute_trade(self, symbol, side, quantity, price):
        cost = quantity * price

        if quantity <= 0 or price <= 0:
            return {"error": "Quantity and price must be greater than zero."}

        if side == "buy" and cost > self.balance:
            return {"error": "Insufficient funds."}

        if side == "buy":
            self.balance -= cost
        elif side == "sell":
            self.balance += cost

        trade = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "status": "filled",
            "balance": self.balance
        }
        self.trades.append(trade)
        return trade
