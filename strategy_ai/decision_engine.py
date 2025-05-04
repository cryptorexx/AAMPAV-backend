# strategy_ai/decision_engine.py

import random
from analysis_ai.market_analyzer import MarketAnalyzer
from portfolio_manager import PortfolioManager
from execution_ai.risk_controller import RiskController
from analysis_ai.market_analyzer import analyze_market_conditions

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

from strategy_ai.market_schema import MarketData

def generate_signal(data: MarketData):
    if data.trend == "up" and data.volatility < 0.3:
        return {"action": "buy"}
    elif data.trend == "down" and data.volatility < 0.3:
        return {"action": "sell"}
    else:
        return {"action": "hold"}
        
def generate_trade_decision(asset_data):
    market_analysis = analyze_market_conditions()
    news_signals = market_analysis.get("news_signals", [])

    decisions = []

    for asset in asset_data:
        symbol = asset.get("symbol")
        score = 0.5  # Neutral baseline score

        # Match relevant news signals
        relevant_signals = [
            signal for signal in news_signals if signal["symbol"] == symbol or signal["symbol"] == "GLOBAL"
        ]

        for signal in relevant_signals:
            score += signal["impact_score"] * 0.2  # Bias the decision upward

        # Clamp score between 0 and 1
        score = min(max(score, 0), 1)

        action = "BUY" if score > 0.6 else "HOLD" if score > 0.4 else "SELL"

        decisions.append({
            "symbol": symbol,
            "action": action,
            "confidence": round(score, 2),
            "news_bias": len(relevant_signals),
        })

    return decisions
