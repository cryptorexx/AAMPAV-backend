# execution_ai/smart_execution.py
from execution_ai.risk_controller import RiskController
from execution_ai.broker_interface import AlpacaBroker

class SmartExecutor:
    def __init__(self):
        self.risk_controller = RiskController()
        self.broker = AlpacaBroker()

    def safe_execute(self, symbol, side, quantity, price):
        trade_cost = quantity * price
        estimated_loss = price * 0.01 * quantity  # Assume 1% potential drop
        is_safe, reason = self.risk_controller.check_risk(100000, trade_cost, estimated_loss)

        if not is_safe:
            return {"status": "rejected", "reason": reason}

        response = self.broker.place_order(symbol, quantity, side)
        return {
            "status": "executed" if "id" in response else "failed",
            "details": response
        }
