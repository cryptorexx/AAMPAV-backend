import os
from cryptography.fernet import Fernet
from encryption_utils import load_decrypted_env_variable
from fastapi import FastAPI, Request, HTTPException, Depends, BackgroundTasks, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from strategy_ai.market_schema import MarketData
from execution_ai.smart_execution import SmartExecutor
from analysis_ai.market_analyzer import MarketAnalyzer
from strategy_ai.decision_engine import generate_signal
from system_maintenance import run_cleanup
from payment_ai.split_manager import create_payment
from payment_ai.split_manager import WalletManager

wallet_manager = WalletManager()

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
API_KEY = os.getenv("API_KEY", "-_k7HtLtIyxUuh2HMj5mSVSvpFUxzYYkmD8asOniC3U")

smart_executor = SmartExecutor()
market_analyzer = MarketAnalyzer()
bot_running = False
logs = []

def verify_api_key(request: Request):
    client_key = request.headers.get("X-API-Key")
    if client_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

    @app.get("/test-broker")
def test_broker(dep=Depends(verify_api_key)):
    from execution_ai.brokers.broker_interface import BrokerInterface
    broker = BrokerInterface()
    return {
        "selected_broker": broker.selected_broker,
        "api_key": broker.api_key,
        "ping_success": broker.handler.get_broker(broker.selected_broker).ping()
    }

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
        
@app.post("/deposit")
def deposit_funds(amount: float = Body(..., embed=True)):
    if amount <= 0:
        return {"error": "Deposit must be greater than zero."}

    # Deposit into collective wallet
    wallet_manager.deposit("collective_wallet", amount)

    # Split 50/50
    split_amount = amount / 2
    wallet_manager.withdraw("collective_wallet", split_amount)
    wallet_manager.deposit("trading_wallet", split_amount)

    return {
        "message": f"${amount} deposited. ${split_amount} sent to trading_wallet. ${split_amount} kept in collective_wallet.",
        "wallets": wallet_manager.get_balances()
    }
    def run_bot():
        global bot_running
        try:
            bot_running = True
            logs.append("Bot started.")
            market_data = market_analyzer.analyze_market("AAPL")
            validated = MarketData(**market_data)
            signal = generate_signal(validated)
            result = smart_executor.safe_execute("AAPL", signal["action"], 10, 150.0)
            logs.append(result)
        except Exception as e:
            logs.append(f"Bot error: {str(e)}")
        finally:
            bot_running = False

    background_tasks.add_task(run_bot)
    return {"message": "Bot started in background"}

@app.post("/stop-bot")
@limiter.limit("3/minute")
def stop_bot(request: Request, dep=Depends(verify_api_key)):
    global bot_running
    if bot_running:
        bot_running = False
        logs.append("Bot stopped by user.")
        return {"message": "Bot stopped"}
    return {"message": "Bot already stopped"}
    from fastapi import Body

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze(request: Request, dep=Depends(verify_api_key)):
    data = await request.json()
    symbol = data.get("symbol")
    if not symbol:
        raise HTTPException(status_code=400, detail="Missing symbol")
    analysis = market_analyzer.analyze_market(symbol)
    return {"analysis": analysis}

@app.post("/trade")
@limiter.limit("5/minute")
async def trade(request: Request, dep=Depends(verify_api_key)):
    data = await request.json()
    symbol = data.get("symbol")
    action = data.get("action")
    quantity = data.get("quantity")
    price = data.get("price")

    if not all([symbol, action, quantity, price]):
        raise HTTPException(status_code=400, detail="Incomplete trade data")

    result = smart_executor.safe_execute(symbol, action, quantity, price)
    return {"result": result}

@app.post("/pay")
@limiter.limit("5/minute")
def generate_payment(request: Request, amount: float = Query(...)):
    return create_payment(amount)

@app.get("/logs")
@limiter.limit("3/minute")
def logs_route(request: Request, dep=Depends(verify_api_key)):
    return {"logs": logs or ["No activity recorded."]}

# --- Global Variables ---
API_KEY = os.getenv("API_KEY", "your_default_key")
broker_api_key = load_decrypted_env_variable()
smart_executor = SmartExecutor()
market_analyzer = MarketAnalyzer()
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
    
@app.post("/receive-royalty")
@limiter.limit("5/minute")
def receive_royalty(amount: float = Query(...), dep=Depends(verify_api_key)):
    result = wallet_manager.split_and_store(amount)
    return {"message": "Royalty received and split", "result": result}
    
@app.get("/wallets")
@limiter.limit("5/minute")
def get_wallets(dep=Depends(verify_api_key)):
    return wallet_manager.get_wallets()

# --- Startup Tasks ---
run_cleanup()

def load_decrypted_env_variable(env_file_path=".env", key_file_path="secret.key"):
    with open(key_file_path, 'rb') as key_file:
        secret_key = key_file.read()

    fernet = Fernet(secret_key)

    with open(env_file_path, 'r') as env_file:
        for line in env_file:
            if line.startswith("ENCRYPTED_API_KEY="):
                encrypted_value = line.strip().split("=", 1)[1]
                decrypted_value = fernet.decrypt(encrypted_value.encode()).decode()
                return decrypted_value

    raise ValueError("ENCRYPTED_API_KEY not found in .env")

# --- Optional Dev Server ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
