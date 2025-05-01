# strategy_ai/decision_engine.py
from analysis_ai.market_analyzer import MarketAnalyzer
from execution_ai.risk_controller import RiskController
from portfolio_manager import PortfolioManager

class DecisionEngine:
    def __init__(self):
        self.analyzer = MarketAnalyzer()
        self.risk_controller = RiskController()
        self.portfolio_manager = PortfolioManager()

    def should_execute_trade(self, symbol, side, quantity, price):
        analysis = self.analyzer.analyze_market(symbol)
        trend = analysis.get("trend", "neutral")
        confidence = analysis.get("confidence", 0.5)

        if trend == "bearish" and side == "buy":
            return False, f"Bearish trend for {symbol}. Avoid buying."
        if trend == "bullish" and side == "sell":
            return False, f"Bullish trend for {symbol}. Avoid selling."

        exposure = self.portfolio_manager.get_exposure().get(symbol, 0)
        if side == "buy" and exposure >= 0.3:
            return False, f"Exposure to {symbol} too high: {exposure * 100:.0f}%"

        trade_cost = quantity * price
        estimated_loss = price * 0.01 * quantity
        is_safe, reason = self.risk_controller.check_risk(100000, trade_cost, estimated_loss)
        if not is_safe:
            return False, reason

        return True, "Trade approved."
