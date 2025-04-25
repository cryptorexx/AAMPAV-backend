import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
bot_running = False
bot_logs = []

@app.get("/status")
def get_status():
    return {"message": "Backend is connected and running successfully."}

@app.post("/start-bot")
def start_bot():
    global bot_running
    if bot_running:
        return {"message": "Bot is already running."}
    bot_running = True
    bot_logs.append("Bot started.")
    return {"message": "Bot started successfully."}

@app.post("/stop-bot")
def stop_bot():
    global bot_running
    if not bot_running:
        return {"message": "Bot is not running."}
    bot_running = False
    bot_logs.append("Bot stopped.")
    return {"message": "Bot stopped successfully."}

@app.get("/logs")
def get_logs():
    return {"logs": bot_logs if bot_logs else ["Bot is not running. No activity to show."]}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("fastapi_app.main:app", host="0.0.0.0", port=port)
