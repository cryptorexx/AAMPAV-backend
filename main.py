# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from execution_ai.smart_execution import SmartExecutor
from analysis_ai.market_analyzer import MarketAnalyzer

app = FastAPI()
smart_executor = SmartExecutor()
market_analyzer = MarketAnalyzer()
bot_running = False
logs = []

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

    result = smart_executor.safe_execute(symbol, side, quantity, price)
    return {"result": result}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    symbol = data.get("symbol")
    analysis = market_analyzer.analyze_market(symbol)
    return {"analysis": analysis}

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
    return {"logs": logs or ["Bot is not running. No activity to show."]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
