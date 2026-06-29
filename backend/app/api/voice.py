from fastapi import APIRouter

from app.schemas.voice_schema import (
    VoiceChatRequest,
    VoiceChatResponse,
)

from app.services.voice_service import (
    ask_voice_assistant,
)

router = APIRouter(
    prefix="/voice",
    tags=["Voice Assistant"],
)


@router.post(
    "/chat",
    response_model=VoiceChatResponse,
)
async def voice_chat(
    request: VoiceChatRequest,
):

    response = await ask_voice_assistant(
        request.message,
        [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in request.history
        ]
    )

    return VoiceChatResponse(
        response=response
    )