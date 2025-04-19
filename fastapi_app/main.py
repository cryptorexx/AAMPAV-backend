# Entrypoint for FastAPI app

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "Backend is running"}