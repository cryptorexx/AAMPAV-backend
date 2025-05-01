# execution_ai/trade_engine.py

from execution_ai.broker_interface import BrokerInterface
from strategy_ai.decision_engine import DecisionEngine
from portfolio_manager import PortfolioManager

class TradeEngine:
    def __init__(self):
        self.broker = BrokerInterface()
        self.decision_engine = DecisionEngine()
        self.portfolio_manager = PortfolioManager()
        self.balance = 100000  # USD
        self.trades = []

    def execute_trade(self, symbol, side, quantity, price):
        cost = quantity * price

        if quantity <= 0 or price <= 0:
            return {"error": "Quantity and price must be greater than zero."}

        # Decision engine check
        decision, reason = self.decision_engine.should_execute_trade(symbol, side, quantity, price)
        if not decision:
            return {"error": reason}

        # Check if funds are sufficient
        if side == "buy" and cost > self.balance:
            return {"error": "Insufficient funds."}

        # Simulate broker execution
        result = self.broker.place_order(symbol, side, quantity, price)
        if result.get("status") != "filled":
            return {"error": "Trade could not be filled by broker."}

        # Update balance
        if side == "buy":
            self.balance -= cost
        elif side == "sell":
            self.balance += cost

        # Update holdings
        self.portfolio_manager.update_holdings(symbol, side, quantity)

        trade = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "status": "filled",
            "balance": self.balance,
            "reason": reason
        }
        self.trades.append(trade)
        return trade
