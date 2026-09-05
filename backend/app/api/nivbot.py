from fastapi import APIRouter
from backend.app.schemas.nivbot import *
from backend.app.services.nivbot_service import NivBotService
import traceback


router = APIRouter(prefix="/nivbot", tags=["NivBot"])


@router.post("/chat")
async def chat(request: NivBotRequest):

    try:
        answer = await NivBotService.chat(
            request.question,
            request.locality_name,
        )

        return {"answer": answer}

    except Exception as e:
       print("================================")
       print("NIVBOT ERROR")
       traceback.print_exc()
       print("================================")
       raise
