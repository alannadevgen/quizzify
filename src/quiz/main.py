from api.router import router as api_router
from fastapi import FastAPI

app = FastAPI(
    title="Quizzify",
)

app.include_router(api_router)
