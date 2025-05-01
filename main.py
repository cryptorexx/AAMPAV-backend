from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from execution_ai.trade_engine import TradeEngine
from analysis_ai.market_analyzer import MarketAnalyzer

app = FastAPI()
trade_engine = TradeEngine()
market_analyzer = MarketAnalyzer()

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

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    analysis = market_analyzer.analyze_market(symbol)
    return {"analysis": analysis}

# Additional endpoints: status, logs, start/stop bot...
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

# main.py (only relevant part shown for integration clarity)

from execution_ai.smart_execution import SmartExecutor
from execution_ai.trade_engine import TradeEngine

# Initialize components
smart_executor = SmartExecutor()
trade_engine = TradeEngine()

@app.post("/trade")
async def trade(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    side = data.get("action")
    quantity = data.get("quantity")
    price = data.get("price")

    # Use SmartExecutor to perform a safe trade
    result = smart_executor.safe_execute(symbol, side, quantity, price)
    return {"result": result}

# Make sure the main.py runs with uvicorn or through Render settings
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
