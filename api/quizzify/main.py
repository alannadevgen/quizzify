import logging.config

from fastapi import FastAPI

from quizzify.routers.v1.albums.router import router as albums_router
from quizzify.routers.v1.artists.router import router as artists_router
from quizzify.routers.v1.auth.router import router as auth_router
from quizzify.routers.v1.questions.router import router as questions_router
from quizzify.routers.v1.songs.router import router as songs_router

# Define the API version prefix
API_VERSION = "/v1"
API_LATEST = "/latest"

# Get root logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Quizzify",
    description="Spotify Music Quizz API",
    version="0.1.0",
    docs_url="/docs",
)


@app.get("/")
def index():
    """Return the API name and description."""
    return {"Quizzify": "Spotify Music Quizz API"}


for prefix in [API_VERSION, API_LATEST]:
    app.include_router(auth_router, prefix=f"{prefix}/auth", tags=["Authentication"])
    app.include_router(albums_router, prefix=f"{prefix}/albums", tags=["Albums"])
    app.include_router(artists_router, prefix=f"{prefix}/artists", tags=["Artists"])
    app.include_router(
        questions_router, prefix=f"{prefix}/questions", tags=["Questions"]
    )
    app.include_router(songs_router, prefix=f"{prefix}/songs", tags=["Songs"])
