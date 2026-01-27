from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat

# Create FastAPI app
app = FastAPI(title="SOORAJ AI Backend")

# Allow React frontend to call this backend
origins = ["http://localhost:3000"]  # React dev server
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
