import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup to allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Status route
@app.get("/status")
def get_status():
    return {"message": "Backend is connected and running successfully."}

# Simulated bot state
bot_state = {"running": False}

# Start bot route
@app.post("/start-bot")
def start_bot():
    bot_state["running"] = True
    return {"message": "Bot started"}

# Stop bot route
@app.post("/stop-bot")
def stop_bot():
    bot_state["running"] = False
    return {"message": "Bot stopped"}

# Logs route (mocked)
@app.get("/logs")
def get_logs():
    if bot_state["running"]:
        return {
            "logs": [
                "Trade executed at $123.45",
                "Profit: $12.00",
                "New trade signal received",
            ]
        }
    else:
        return {"logs": ["Bot is not running. No activity to show."]}

# Server startup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
