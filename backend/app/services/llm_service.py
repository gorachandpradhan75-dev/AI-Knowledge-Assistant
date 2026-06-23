"""
LLM service: a single abstraction over the chat-completion backend.

Two providers are supported out of the box:
  - "ollama"            -> self-hosted Llama 3 / Gemma via Ollama's HTTP API
  - "openai_compatible" -> any OpenAI-compatible endpoint

Routers/services never talk to the provider directly.
"""
from collections.abc import AsyncIterator

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging_config import logger

ChatMessages = list[dict[str, str]]


class LLMService:
    def __init__(self) -> None:
        self.provider = settings.LLM_PROVIDER

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    async def chat(self, messages: ChatMessages, temperature: float = 0.4) -> str:
        if self.provider == "ollama":
            return await self._ollama_chat(messages, temperature)
        return await self._openai_compatible_chat(messages, temperature)

    async def chat_stream(self, messages: ChatMessages, temperature: float = 0.4) -> AsyncIterator[str]:
        if self.provider == "ollama":
            async for chunk in self._ollama_chat_stream(messages, temperature):
                yield chunk
        else:
            async for chunk in self._openai_compatible_chat_stream(messages, temperature):
                yield chunk

    async def _ollama_chat(self, messages: ChatMessages, temperature: float) -> str:
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": settings.OLLAMA_CHAT_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip()

    async def _ollama_chat_stream(self, messages: ChatMessages, temperature: float):
        url = f"{settings.OLLAMA_BASE_URL}/api/chat"
        payload = {
            "model": settings.OLLAMA_CHAT_MODEL,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature},
        }
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    import json as _json

                    chunk = _json.loads(line)
                    token = chunk.get("message", {}).get("content", "")
                    if token:
                        yield token
                    if chunk.get("done"):
                        break

    async def _openai_compatible_chat(self, messages: ChatMessages, temperature: float) -> str:
        url = f"{settings.OPENAI_COMPATIBLE_BASE_URL}/chat/completions"
        headers = {"Authorization": f"Bearer {settings.OPENAI_COMPATIBLE_API_KEY}"}
        payload = {
            "model": settings.OPENAI_COMPATIBLE_MODEL,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()

    async def _openai_compatible_chat_stream(self, messages: ChatMessages, temperature: float):
        url = f"{settings.OPENAI_COMPATIBLE_BASE_URL}/chat/completions"
        headers = {"Authorization": f"Bearer {settings.OPENAI_COMPATIBLE_API_KEY}"}
        payload = {
            "model": settings.OPENAI_COMPATIBLE_MODEL,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    data_str = line[len("data:"):].strip()
                    if data_str == "[DONE]":
                        break
                    import json as _json

                    chunk = _json.loads(data_str)
                    delta = chunk["choices"][0]["delta"].get("content")
                    if delta:
                        yield delta

    async def health_check(self) -> bool:
        try:
            await self.chat([{"role": "user", "content": "ping"}], temperature=0.0)
            return True
        except Exception as exc:
            logger.warning(f"LLM health check failed: {exc}")
            return False


llm_service = LLMService()