import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample trade logs list
trade_logs = []

class TradeSignal(BaseModel):
    symbol: str
    action: str
    quantity: int

@app.get("/status")
def get_status():
    return {"message": "Backend is connected and running successfully."}

@app.get("/analyze")
def analyze_market():
    return {
        "symbol": "AAPL",
        "action": "buy",
        "confidence": 0.89,
        "notes": "AI suggests a bullish trend based on recent analysis."
    }

@app.post("/execute")
def execute_trade(signal: TradeSignal):
    trade_logs.append(signal)
    return {"message": "Trade executed", "trade": signal}

@app.get("/logs")
def get_logs():
    return {"trades": trade_logs}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)
