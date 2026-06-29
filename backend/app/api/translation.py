from fastapi import APIRouter

from app.schemas.translation_schema import (
    TranslationRequest,
    TranslationResponse,
)
from app.services.translation_service import (
    translate_text,
)

router = APIRouter(
    prefix="/translation",
    tags=["Translation"]
)


@router.post(
    "/translate",
    response_model=TranslationResponse,
)
async def translate(
    request: TranslationRequest,
):

    translated_text = await translate_text(
        request.text,
        request.target_language,
    )

    return TranslationResponse(
        original_text=request.text,
        translated_text=translated_text,
        target_language=request.target_language,
    )