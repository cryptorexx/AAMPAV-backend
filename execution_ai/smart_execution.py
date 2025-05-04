# execution_ai/smart_execution.py

import time
from execution_ai.risk_controller import RiskController
from execution_ai.brokers.broker_interface import BrokerInterface
from strategy_ai.decision_engine import DecisionEngine
from portfolio_manager import PortfolioManager
from execution_ai.stealth_behaviors import apply_stealth

class SmartExecutor:
    def __init__(self):
        self.risk_controller = RiskController()
        self.broker = BrokerInterface()
        self.decision_engine = DecisionEngine()
        self.portfolio = PortfolioManager()

    def safe_execute(self, symbol, side, quantity, price):
        # Decision Engine filters it first
        allowed, reason = self.decision_engine.should_execute_trade(symbol, side, quantity, price)
        if not allowed:
            return {
                "status": "rejected",
                "reason": reason
            }

        # Apply stealth behavior (random delay, quantity fuzzing, etc.)
        stealth_result = apply_stealth(symbol, side, quantity, price)
        quantity = stealth_result["quantity"]
        price = stealth_result["price"]
        delay = stealth_result["delay"]
        
        time.sleep(delay)  # Simulate hesitation

        # Now execute trade
        trade_result = self.broker.place_order(symbol, quantity, side)
        if not trade_result or "error" in trade_result:
            return {
                "status": "failed",
                "details": trade_result.get("error", "Unknown broker error")
            }

        self.portfolio.update_holdings(symbol, side, quantity, price)

        return {
            "status": "executed_with_stealth",
            "details": trade_result,
            "stealth_used": stealth_result
        }
wallet_manager = WalletManager()
