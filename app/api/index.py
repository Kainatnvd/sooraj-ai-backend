from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router

app = FastAPI(title="SOORAJ AI Backend (Vercel)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://YOUR-FRONTEND.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/chat")

@app.get("/")
def root():
    return {"message": "SOORAJ AI Backend running on Vercel"}
