from app.services.llm_service import llm_service


async def ask_voice_assistant(
    message: str,
    history: list = None,
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Remember the conversation context."
            ),
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    return await llm_service.chat(
        messages,
        temperature=0.5,
    )