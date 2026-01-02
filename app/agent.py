from openai import OpenAI
from .config.settings import settings


class Agent:
    def __init__(self, model: str = "gpt-4.1"):
        self.model = model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def answer(self, query: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=query,
            instructions="You are a helpful assistant ready to answer any user query",
        )
        return response.output_text
