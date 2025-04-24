import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aampav-frontend.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ This is the root route that frontend is checking!
@app.get("/")
def root():
    return {"message": "Hello from AAMPAV backend!"}

# ✅ This route is useful for backend-specific health checks
@app.get("/status")
def get_status():
    return {"message": "Backend is connected and running successfully."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
