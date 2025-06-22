from datetime import date

from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek

from services.llm.base import LLMClient
from services.time_utils import async_perf_counter


class DeeSeekClient(LLMClient):
    def __init__(self):
        self.rag_client = ChatDeepSeek(model="deepseek-chat", temperature=0.2)
        self.response_client = ChatDeepSeek(model="deepseek-chat", temperature=0.8)

    @async_perf_counter
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

    @async_perf_counter
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
        return self.safe_json(response.content)
