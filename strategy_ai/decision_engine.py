# strategy_ai/decision_engine.py

from analysis_ai.market_analyzer import analyze_market
from execution_ai.risk_controller import RiskController
from portfolio_manager import PortfolioManager

class DecisionEngine:
    def __init__(self):
        self.risk_controller = RiskController()
        self.portfolio_manager = PortfolioManager()

    def should_execute_trade(self, symbol, side, quantity, price):
        # Analyze the market condition
        analysis = analyze_market(symbol)
        trend = analysis.get("trend", "neutral")
        confidence = analysis.get("confidence", 0.5)

        # Check for safe market trend
        if trend == "bearish" and side == "buy":
            return False, f"Market trend for {symbol} is bearish. Avoid buying."

        if trend == "bullish" and side == "sell":
            return False, f"Market trend for {symbol} is bullish. Avoid selling."

        # Check for excessive exposure
        exposure = self.portfolio_manager.get_exposure().get(symbol, 0)
        if side == "buy" and exposure >= 0.3:
            return False, f"Exposure to {symbol} too high: {exposure*100:.0f}%. Limit buying."

        # Risk assessment
        is_risky, reason = self.risk_controller.is_trade_risky(symbol, side, quantity, price)
        if is_risky:
            return False, f"Trade rejected due to risk: {reason}"

        return True, "Trade conditions are acceptable."
