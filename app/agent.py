from openai import OpenAI
from .config.settings import settings
from langfuse import observe, Langfuse


class Agent:
    def __init__(self, model: str = "gpt-4.1"):
        self.model = model
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.langfuse = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            base_url=settings.langfuse_base_url,
        )

    @observe(as_type="generation", capture_input=False, capture_output=False)
    def answer(self, query: str) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": query},
        ]

        response = self.client.responses.create(
            model=self.model,
            input=messages,  # type: ignore
        )

        self.langfuse.update_current_generation(
            input=messages,
            output=response.output_text,
            usage_details={
                "input": getattr(response.usage, "input_tokens", 0),
                "output": getattr(response.usage, "output_tokens", 0),
            },
        )

        return response.output_text
