from app.config import settings
import httpx

class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.DEFAULT_MODEL
        self.api_key = settings.OPENAI_API_KEY

    async def generate(self, prompt: str) -> str:
        if self.provider == "openai":
            return await self._openai_generate(prompt)
        else:
            return f"[LLM Mock] {prompt[:200]}..."

    async def _openai_generate(self, prompt: str) -> str:
        if not self.api_key:
            return "[Error] OPENAI_API_KEY not set"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a helpful TRPG Game Master. Always respond with valid JSON when requested."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": settings.TEMPERATURE
                },
                timeout=60.0
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]
