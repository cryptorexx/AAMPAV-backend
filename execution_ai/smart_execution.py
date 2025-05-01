# smart_execution.py

from execution_ai.risk_controller import RiskController
from execution_ai.broker_interface import BrokerInterface

class SmartExecution:
    def __init__(self):
        self.risk_controller = RiskController()
        self.broker = BrokerInterface()

    def execute(self, symbol, side, quantity, price):
        # Evaluate risk first
        if not self.risk_controller.is_trade_safe(symbol, side, quantity, price):
            return {
                "status": "rejected",
                "reason": "Trade violates risk parameters"
            }

        # If risk check passes, execute trade
        trade_result = self.broker.place_order(symbol, side, quantity, price)

        return {
            "status": "executed" if trade_result else "failed",
            "details": trade_result or "Broker rejected the order"
        }
