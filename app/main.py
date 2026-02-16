import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import chat

# ---------- Create FastAPI app ----------
app = FastAPI(title="SOORAJ AI Backend")

# Allow React frontend to call this backend
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(chat.router, prefix="/api/chat")

# Health check / root endpoint
@app.get("/")
def root():
    return {"message": "SOORAJ AI Backend running!"}

# ---------- Run the app for Cloud Run ----------
if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run
    port = int(os.environ.get("PORT", 8080))
    # Listen on 0.0.0.0 so the container is accessible externally
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
