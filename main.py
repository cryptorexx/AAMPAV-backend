# main.py

from system_maintenance import run_cleanup
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from execution_ai.smart_execution import SmartExecutor
from analysis_ai.market_analyzer import MarketAnalyzer
from fastapi import Query
from payment_processor import create_payment
from fastapi import FastAPI, Request, HTTPException, Depends
from execution_ai.smart_execution import start_bot
from execution_ai.logs_handler import get_logs
import os

app = FastAPI()

# --- API KEY SETUP ---
API_KEY = os.getenv("API_KEY", "-_k7HtLtIyxUuh2HMj5mSVSvpFUxzYYkmD8asOniC3U")

def verify_api_key(request: Request):
    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

# --- SECURE ROUTES ---
@app.get("/status")
def get_status(dep=Depends(verify_api_key)):
    return {"status": "running"}

@app.post("/start-bot")
def start_bot_route(dep=Depends(verify_api_key)):
    return start_bot()

@app.get("/logs")
def logs_route(dep=Depends(verify_api_key)):
    return get_logs()

from fastapi import FastAPI, Request, HTTPException, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from execution_ai.smart_execution import start_bot
from execution_ai.logs_handler import get_logs
import os

app = FastAPI()

# --- RATE LIMITER SETUP ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- API KEY SETUP ---
API_KEY = os.getenv("API_KEY", "-_k7HtLtIyxUuh2HMj5mSVSvpFUxzYYkmD8asOniC3U")

def verify_api_key(request: Request):
    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

# --- PROTECTED AND LIMITED ROUTES ---
@app.get("/status")
@limiter.limit("10/minute")  # 10 calls per minute per IP
def get_status(request: Request, dep=Depends(verify_api_key)):
    return {"status": "running"}

@app.post("/start-bot")
@limiter.limit("5/minute")
def start_bot_route(request: Request, dep=Depends(verify_api_key)):
    return start_bot()

@app.get("/logs")
@limiter.limit("3/minute")
def logs_route(request: Request, dep=Depends(verify_api_key)):
    return get_logs()

run_cleanup()

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

@app.post("/pay")
def generate_payment(amount: float = Query(...)):
    return create_payment(amount)

app = FastAPI()
smart_executor = SmartExecutor()
market_analyzer = MarketAnalyzer()
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
    return {"logs": logs or ["Bot is not running. No activity to show."]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
