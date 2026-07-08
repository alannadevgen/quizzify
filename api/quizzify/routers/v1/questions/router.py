from fastapi import APIRouter

from quizzify.routers.v1.questions import service

router = APIRouter()


@router.get(
    path="/create",
    # response_model=List[Dict],
    summary="Create a question ",
    description=("Create a question based on the user's top artists from Spotify."),
)
async def create_question():
    """Call the question service to create a random question."""
    return service.create_question()
