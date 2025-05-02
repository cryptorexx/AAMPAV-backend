# strategy_ai/decision_engine.py

import random
from analysis_ai.market_analyzer import MarketAnalyzer
from portfolio_manager import PortfolioManager
from execution_ai.risk_controller import RiskController

class DecisionEngine:
    def __init__(self):
        self.market_analyzer = MarketAnalyzer()
        self.portfolio = PortfolioManager()
        self.risk = RiskController()

    def should_trade(self, symbol, price, side, quantity):
        # Step 1: Analyze market sentiment
        analysis = self.market_analyzer.analyze_market(symbol)
        trend = analysis.get("trend", "neutral")
        confidence = analysis.get("confidence", 0.5)

        # Step 2: Stealth-like human decision randomness
        if random.random() < 0.1:
            return False, "Human-like hesitation triggered. No trade."

        # Step 3: Simulated trend strategy
        if trend == "bullish" and side == "buy" and confidence > 0.6:
            decision = True
        elif trend == "bearish" and side == "sell" and confidence > 0.6:
            decision = True
        else:
            return False, f"Market sentiment not aligned. Trend: {trend}, Confidence: {confidence}"

        # Step 4: Check risk
        is_safe, reason = self.risk.check_risk(self.portfolio.get_cash(), price * quantity, price * quantity * 0.05)
        if not is_safe:
            return False, f"Risk rejected: {reason}"

        return decision, f"Trade approved. Trend: {trend}, Confidence: {confidence}"
