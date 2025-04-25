import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State
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
    return {"message": "Bot started."}

@app.post("/stop-bot")
def stop_bot():
    global bot_running
    if bot_running:
        bot_running = False
        bot_logs.append("Bot stopped.")
    return {"message": "Bot stopped."}

@app.get("/logs")
def get_logs():
    if not bot_running and not bot_logs:
        return {"logs": ["Bot is not running. No activity to show."]}
    return {"logs": bot_logs}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
