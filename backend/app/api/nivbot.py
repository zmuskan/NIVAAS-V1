from fastapi import APIRouter
from backend.app.schemas.nivbot import *
from backend.app.services.nivbot_service import NivBotService
import traceback


router = APIRouter(prefix="/nivbot", tags=["NivBot"])


@router.post("/chat")
async def chat(request: NivBotRequest):

    try:
        answer = await NivBotService.chat(
            question=request.question,
            locality_name=request.locality_name,
            mode=request.mode,
            compare_names=request.compare_names,
        )

        return {"answer": answer}

    except Exception as e:
       print("================================")
       print("NIVBOT ERROR")
       traceback.print_exc()
       print("================================")
       raise
