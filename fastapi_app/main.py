from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simulated in-memory bot state and logs
bot_status = {"running": False}
trade_logs = []

@app.get("/status")
def get_status():
    return {"message": "Backend is connected and running successfully."}

@app.post("/start-bot")
def start_bot():
    if not bot_status["running"]:
        bot_status["running"] = True
        trade_logs.append("Bot started.")
    return {"status": "Bot started"}

@app.post("/stop-bot")
def stop_bot():
    if bot_status["running"]:
        bot_status["running"] = False
        trade_logs.append("Bot stopped.")
    return {"status": "Bot stopped"}

@app.get("/logs")
def get_logs():
    return {"logs": trade_logs}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port)
