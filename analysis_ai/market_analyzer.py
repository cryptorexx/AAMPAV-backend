# analysis_ai/market_analyzer.py

import random
from datetime import datetime, timedelta

def generate_news_signals_from_api():
    # Placeholder logic — replace with your actual API call
    return [
        {"symbol": "AAPL", "signal": "positive", "timestamp": datetime.utcnow()},
        {"symbol": "TSLA", "signal": "negative", "timestamp": datetime.utcnow()}
    ]

def cleanup_old_signals(news_signals, max_age_minutes=60):
    cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)
    return [s for s in news_signals if s.get("timestamp") and s["timestamp"] >= cutoff]

def fetch_news():
    sample_headlines = [
        {"title": "China cuts interest rates amid global slowdown", "source": "Reuters"},
        {"title": "Oil prices surge after Middle East tensions escalate", "source": "Bloomberg"},
        {"title": "US Fed hints at prolonged rate hikes", "source": "CNBC"},
        {"title": "Tech export bans imposed on Taiwan", "source": "Yahoo Finance"},
        {"title": "Russia announces new sanctions on European gas", "source": "BBC"},
    ]

    geopolitical_signals = []

    for headline in sample_headlines:
        impact_score = round(random.uniform(0.5, 1.0), 2)
        symbol = infer_symbol_from_headline(headline["title"])
        geopolitical_signals.append({
            "timestamp": datetime.utcnow(),
            "title": headline["title"],
            "source": headline["source"],
            "impact_score": impact_score,
            "symbol": symbol,
        })

    return geopolitical_signals

def infer_symbol_from_headline(title):
    title = title.lower()
    if "oil" in title or "gas" in title:
        return "XOM"
    elif "tech" in title or "taiwan" in title:
        return "AAPL"
    elif "china" in title:
        return "BABA"
    elif "fed" in title or "interest" in title:
        return "^GSPC"
    elif "russia" in title:
        return "GAZP"
    return "GLOBAL"

def analyze_market_conditions():
    news_signals = generate_news_signals_from_api()
    news_signals = cleanup_old_signals(news_signals)

    return {
        "market_trends": "Bullish",
        "volatility": "Moderate",
        "news_signals": news_signals
    }

class MarketAnalyzer:
    def __init__(self):
        self.sentiment = "neutral"

    def analyze_market(self, symbol):
        trend = random.choice(["bullish", "bearish", "neutral"])
        confidence = round(random.uniform(0.5, 1.0), 2)
        self.sentiment = trend
        return {
            "symbol": symbol,
            "trend": trend,
            "confidence": confidence
        }
