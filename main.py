import os
from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from strategy_ai.market_schema import MarketData
from execution_ai.smart_execution import SmartExecutor
from analysis_ai.market_analyzer import MarketAnalyzer
from strategy_ai.decision_engine import generate_signal
from execution_ai.trade_engine import TradeEngine
from execution_ai.logs_handler import get_logs as fetch_logs
from payment_processor import create_payment
from encryption_utils import load_decrypted_env_variable
from system_maintenance import run_cleanup

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Variables ---
API_KEY = os.getenv("API_KEY", "your_default_key")
broker_api_key = load_decrypted_env_variable()
smart_executor = SmartExecutor()
market_analyzer = MarketAnalyzer()
trade_engine = TradeEngine()
bot_running = False
logs = []

# --- Security ---
def verify_api_key(request: Request):
    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

# --- Core Logic ---
def start_bot_logic():
    global bot_running
    market_data = market_analyzer.analyze_market("AAPL")
    validated_data = MarketData(**market_data)
    signal = generate_signal(validated_data)
    result = smart_executor.safe_execute("AAPL", signal["action"], 10, 150.0)
    logs.append(result)

# --- Routes ---
@app.get("/status")
@limiter.limit("10/minute")
def get_status(request: Request, dep=Depends(verify_api_key)):
    return {"status": "Running" if bot_running else "Stopped"}

@app.post("/start-bot")
@limiter.limit("5/minute")
def start_bot_route(background_tasks: BackgroundTasks, request: Request, dep=Depends(verify_api_key)):
    global bot_running
    if bot_running:
        return {"message": "Bot already running"}

    try:
        def run_bot():
            global bot_running
            bot_running = True
            logs.append("Bot started.")
            start_bot_logic()

        background_tasks.add_task(run_bot)
        return {"message": "Bot started in background"}
    except Exception as e:
        return {"error": f"Failed to start bot: {str(e)}"}

@app.post("/stop-bot")
def stop_bot(dep=Depends(verify_api_key)):
    global bot_running
    if bot_running:
        bot_running = False
        logs.append("Bot stopped.")
        return {"message": "Bot stopped"}
    return {"message": "Bot already stopped"}

@app.get("/logs")
@limiter.limit("3/minute")
def logs_route(request: Request, dep=Depends(verify_api_key)):
    return {"logs": logs or ["Bot is not running. No activity to show."]}

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

@app.post("/pay")
def generate_payment(amount: float = Query(...)):
    return create_payment(amount)

# --- Startup Tasks ---
run_cleanup()

# --- Optional Dev Server ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
