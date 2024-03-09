import logging.config

from fastapi import FastAPI

from quizzify.api.albums.router import router as albums_router
from quizzify.api.artists.router import router as artists_router
from quizzify.api.auth.router import router as auth_router
from quizzify.api.questions.router import router as questions_router
from quizzify.api.songs.router import router as songs_router

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
app.include_router(albums_router, prefix="/albums", tags=["Albums"])
app.include_router(artists_router, prefix="/artists", tags=["Artists"])
app.include_router(questions_router, prefix="/questions", tags=["Questions"])
app.include_router(songs_router, prefix="/songs", tags=["Songs"])
