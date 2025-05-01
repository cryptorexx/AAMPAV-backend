import random
from .broker_stub import BrokerStub

class SmartExecutionAI:
    def __init__(self):
        self.broker = BrokerStub()
        self.min_confidence = 0.6
        self.max_risk = 0.3  # Allowable % of balance at risk per trade

    def should_execute(self, analysis_result):
        """
        Decide whether to execute a trade based on analysis result.
        """
        trend = analysis_result.get("trend")
        confidence = analysis_result.get("confidence", 0)

        if confidence < self.min_confidence:
            return {"execute": False, "reason": "Low confidence"}

        if trend not in ["bullish", "bearish"]:
            return {"execute": False, "reason": "Unclear trend"}

        return {"execute": True, "reason": "Meets conditions"}

    def execute_trade(self, symbol, analysis_result):
        """
        Safely execute the trade if conditions are met.
        """
        decision = self.should_execute(analysis_result)
        if not decision["execute"]:
            return {"status": "skipped", "reason": decision["reason"]}

        side = "buy" if analysis_result["trend"] == "bullish" else "sell"
        price = self.broker.get_price(symbol)
        quantity = round((self.broker.get_balance() * self.max_risk) / price, 2)

        result = self.broker.place_order(symbol, side, quantity, price)
        return result
