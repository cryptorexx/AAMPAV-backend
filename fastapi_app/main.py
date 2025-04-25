import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bot state and logs
bot_running = False
bot_logs = []

@app.get("/status")
def get_status():
    return {"message": "Backend is connected and running successfully."}

@app.post("/start-bot")
def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        bot_logs.append("Bot started.")
        return {"message": "Bot started successfully."}
    return {"message": "Bot is already running."}

@app.post("/stop-bot")
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        bot_logs.append("Bot stopped.")
        return {"message": "Bot stopped successfully."}
    return {"message": "Bot is already stopped."}

@app.get("/logs")
def get_logs():
    if bot_logs:
        return {"logs": bot_logs}
    return {"logs": ["Bot is not running. No activity to show."]}

# Start the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
