from datetime import date

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from services.llm.base import LLMClient


class OpenAiClient(LLMClient):
    def __init__(self):
        self.rag_client = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        self.response_client = ChatOpenAI(model="gpt-4o-mini", temperature=0.8)

    async def extract_rag(self, history: list, system_prompt: str, lang="ru") -> dict:
        prompt = ChatPromptTemplate.from_template(system_prompt)
        chain = prompt | self.rag_client
        response = await chain.ainvoke(
            input={
                "history": history,
                "today_date": date.today().isoformat(),
                "today_year": str(date.today().year),
            }
        )

        return self.safe_json(response.content)

    async def generate_response(
        self, history: list, system_prompt: str, lang="en"
    ) -> dict:
        prompt = ChatPromptTemplate.from_template(system_prompt)
        chain = prompt | self.response_client
        response = await chain.ainvoke(
            input={
                "history": history,
            }
        )
        return self.safe_json(response)
