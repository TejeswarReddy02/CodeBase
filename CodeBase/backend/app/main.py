from fastapi import FastAPI

from app.api.repository import router as repository_router


app = FastAPI(
    title="CodeBase AI",
    description="AI-powered repository code understanding system",
    version="0.1.0"
)


app.include_router(
    repository_router
)


@app.get("/")
def root():
    return {
        "message": "CodeBase AI backend is running"
    }