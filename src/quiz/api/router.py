from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def default_route():
    """Return the API name and description."""
    return {"Quizzify": "Music Quiz API"}
