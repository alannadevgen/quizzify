import logging.config

from fastapi import FastAPI

from api.auth.router import router as auth_router
from api.songs import router as songs_router

# get root logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Quizzify",
    description="Music Quiz API",
    version="0.1.0",
    docs_url="/docs",
)


@app.get("/")
def index():
    """Return the API name and description."""
    return {"Quizzify": "Music Quiz API"}


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(songs_router, prefix="/songs", tags=["Songs"])
