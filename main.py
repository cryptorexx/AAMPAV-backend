from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from execution_ai.trade_engine import TradeEngine

app = FastAPI()
trade_engine = TradeEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/trade")
async def trade(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    side = data.get("action")
    quantity = data.get("quantity")
    price = data.get("price")

    result = trade_engine.execute_trade(symbol, side, quantity, price)
    return {"result": result}

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # currently open
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot_running = False
logs = []

@app.get("/status")
def get_status():
    return {"status": "Running" if bot_running else "Stopped"}

@app.post("/start-bot")
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        logs.append("Bot started.")
        return {"message": "Bot started"}
    return {"message": "Bot already running"}

@app.post("/stop-bot")
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        logs.append("Bot stopped.")
        return {"message": "Bot stopped"}
    return {"message": "Bot already stopped"}

@app.get("/logs")
def get_logs():
    return {"logs": logs if logs else ["Bot is not running. No activity to show."]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)

