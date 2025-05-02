# execution_ai/smart_execution.py

from execution_ai.risk_controller import RiskController
from execution_ai.brokers.broker_interface import BrokerInterface
from strategy_ai.decision_engine import DecisionEngine
from portfolio_manager import PortfolioManager

class SmartExecutor:
    def __init__(self):
        self.risk_controller = RiskController()
        self.broker = BrokerInterface()
        self.decision_engine = DecisionEngine()
        self.portfolio = PortfolioManager()

    def safe_execute(self, symbol, side, quantity, price):
        # Use decision engine first
        allowed, reason = self.decision_engine.should_execute_trade(symbol, side, quantity, price)
        if not allowed:
            return {
                "status": "rejected",
                "reason": reason
            }

        # Execute if approved
        trade_result = self.broker.place_order(symbol, quantity, side)
        if not trade_result or "error" in trade_result:
            return {
                "status": "failed",
                "details": trade_result.get("error", "Unknown broker error")
            }

        self.portfolio.update_holdings(symbol, side, quantity, price)

        return {
            "status": "executed",
            "details": trade_result
        }
