from app.services.llm_service import llm_service


async def translate_text(
    text: str,
    target_language: str,
) -> str:

    prompt = f"""
Translate the following text into {target_language}.

Text:
{text}

Return only the translated text.
"""

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    return await llm_service.chat(
        messages,
        temperature=0.2,
    )