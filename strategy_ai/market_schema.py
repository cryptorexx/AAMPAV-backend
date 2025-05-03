# strategy_ai/market_schema.py

from pydantic import BaseModel

class MarketData(BaseModel):
    trend: str
    volatility: float
