from fastapi import FastAPI, Request, HTTPException, Depends, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from encryption_utils import load_decrypted_env_variable
from strategy_ai.market_schema import MarketData
from analysis_ai.market_analyzer import MarketAnalyzer
from execution_ai.smart_execution import SmartExecutor
from payment_ai.split_manager import WalletManager
import os

app = FastAPI()

# --- Setup ---
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

API_KEY = os.getenv("API_KEY", "your_default_key")

def verify_api_key(request: Request):
    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

# --- Initialize Components ---
smart_executor = SmartExecutor()
market_analyzer = MarketAnalyzer()
wallet_manager = WalletManager()
bot_running = False
logs = []

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

    def run_bot():
        global bot_running
        try:
            bot_running = True
            logs.append("Bot started")
            market_data = market_analyzer.analyze_market("AAPL")
            validated_data = MarketData(**market_data)
            signal = smart_executor.decision_engine.generate_signal(validated_data)
            result = smart_executor.safe_execute("AAPL", signal["action"], 10, 150.0)
            logs.append(result)
        except Exception as e:
            logs.append(f"Error: {str(e)}")

    background_tasks.add_task(run_bot)
    return {"message": "Bot started in background"}

@app.post("/stop-bot")
@limiter.limit("5/minute")
def stop_bot(request: Request, dep=Depends(verify_api_key)):
    global bot_running
    if bot_running:
        bot_running = False
        logs.append("Bot stopped")
        return {"message": "Bot stopped"}
    return {"message": "Bot was not running"}

@app.get("/logs")
@limiter.limit("3/minute")
def get_logs(request: Request, dep=Depends(verify_api_key)):
    return {"logs": logs or ["No activity yet."]}

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
@limiter.limit("5/minute")
def generate_payment(request: Request, amount: float = Query(...), dep=Depends(verify_api_key)):
    split_result = wallet_manager.split_and_store(amount)
    logs.append(f"Payment processed: {split_result}")
    return {"message": "Payment collected", "details": split_result}

# Load and use decrypted credentials on startup
broker_api_key = load_decrypted_env_variable()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
