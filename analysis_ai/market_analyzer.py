import random
from datetime import datetime, timedelta

class MarketAnalyzer:
    def __init__(self):
        self.sentiment = "neutral"

    def generate_news_signals_from_api():
    # Placeholder logic — replace with your actual API call
    return [
        {"symbol": "AAPL", "signal": "positive"},
        {"symbol": "TSLA", "signal": "negative"}
    ]

    def analyze_market(self, symbol):
        # Placeholder logic: simulate basic analysis
        trend = random.choice(["bullish", "bearish", "neutral"])
        confidence = round(random.uniform(0.5, 1.0), 2)
        
        self.sentiment = trend
        return {
            "symbol": symbol,
            "trend": trend,
            "confidence": confidence
        }
    def analyze_market():
        # TODO: Real analysis logic
        return {"trend": "up", "volatility": 0.25}
        
import random
from datetime import datetime

def fetch_news():
    # Simulated geopolitical headlines (replace with NewsAPI/GDELT later)
    sample_headlines = [
        {"title": "China cuts interest rates amid global slowdown", "source": "Reuters"},
        {"title": "Oil prices surge after Middle East tensions escalate", "source": "Bloomberg"},
        {"title": "US Fed hints at prolonged rate hikes", "source": "CNBC"},
        {"title": "Tech export bans imposed on Taiwan", "source": "Yahoo Finance"},
        {"title": "Russia announces new sanctions on European gas", "source": "BBC"},
    ]

    geopolitical_signals = []

    for headline in sample_headlines:
        impact_score = round(random.uniform(0.5, 1.0), 2)  # Simulated impact
        symbol = infer_symbol_from_headline(headline["title"])
        geopolitical_signals.append({
            "timestamp": datetime.utcnow().isoformat(),
            "title": headline["title"],
            "source": headline["source"],
            "impact_score": impact_score,
            "symbol": symbol,
        })

    return geopolitical_signals

def infer_symbol_from_headline(title):
    title = title.lower()
    if "oil" in title or "gas" in title:
        return "XOM"  # ExxonMobil
    elif "tech" in title or "taiwan" in title:
        return "AAPL"  # Apple
    elif "china" in title:
        return "BABA"  # Alibaba
    elif "fed" in title or "interest" in title:
        return "^GSPC"  # S&P 500
    elif "russia" in title:
        return "GAZP"  # Gazprom (or oil ETF)
    else:
        return "GLOBAL"

def analyze_market_conditions():
    # Existing market data analysis (if any)
    ...
    
    # New: Fetch geopolitical news
    news_signals = fetch_news()
    
    return {
        "market_trends": "Bullish",
        "volatility": "Moderate",
        "news_signals": news_signals
    }
    
# After fetching news_signals from your source
news_signals = generate_news_signals_from_api()  # Or however you get them
news_signals = cleanup_old_signals(news_signals)

def cleanup_old_signals(news_signals, max_age_minutes=60):
    cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)
    return [s for s in news_signals if s["timestamp"] >= cutoff]
