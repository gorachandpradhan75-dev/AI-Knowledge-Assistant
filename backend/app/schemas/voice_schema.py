from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class VoiceChatRequest(BaseModel):
    message: str
    history: List[Message] = []


class VoiceChatResponse(BaseModel):
    response: str