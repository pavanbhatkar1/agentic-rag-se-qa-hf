from openai import OpenAI

from app.core.config import settings


class HuggingFaceClient:
    """LLM client using Hugging Face's OpenAI-compatible inference endpoint."""

    def __init__(self, model: str | None = None, temperature: float = 0.0):
        if not settings.hf_token:
            raise ValueError("HF_TOKEN is not configured.")

        self.model = model or settings.hf_model
        self.temperature = temperature
        self.client = OpenAI(
            base_url=settings.hf_base_url,
            api_key=settings.hf_token,
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=settings.hf_max_new_tokens,
        )
        return response.choices[0].message.content or ""
