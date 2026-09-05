from fastapi import APIRouter

from backend.app.schemas.nivbot import (
    NivBotRequest,
    NivBotResponse,
)

from backend.app.services.nivbot_service import (
    NivBotService,
)

router = APIRouter(
    prefix="/nivbot",
    tags=["NivBot"],
)


@router.post(
    "/chat",
    response_model=NivBotResponse,
)
async def chat(payload: NivBotRequest):

    answer = await NivBotService.chat(
        payload.question,
        payload.locality_context,
    )

    return NivBotResponse(
        answer=answer
    )
