import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import chat

# Create FastAPI app
app = FastAPI(title="SOORAJ AI Backend")

# Allow React frontend to call this backend
origins = [
    "https://soorajcrop.vercel.app",
    "https://soorajcropsciences.com",
    "https://www.soorajcropsciences.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat routes
app.include_router(chat.router, prefix="/api/chat")

@app.get("/")
def root():
    return {"message": "SOORAJ AI Backend running!"}


# 👇 IMPORTANT FOR CLOUD RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run provides PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)
