import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated bot state and logs
bot_running = False
logs = []

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"INCOMING REQUEST: {request.method} {request.url}")
    response = await call_next(request)
    return response

@app.get("/status")
def get_status():
    if bot_running:
        return {"message": "Bot is running"}
    return {"message": "Bot is stopped"}

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
    return {"logs": logs if logs else ["No activity recorded yet."]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
