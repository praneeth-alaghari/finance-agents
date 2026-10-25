import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ai_core.providers.base import BaseLLMProvider

load_dotenv()


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, model=None, api_key=None, **kwargs):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._kwargs = kwargs
        self._llm = None

    def _get_llm(self):
        if self._llm is None:
            self._llm = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                timeout=120.0,
                **self._kwargs,
            )
        return self._llm

    def generate(self, prompt, system_instruction=None, **kwargs):
        messages = [("system", system_instruction), ("user", prompt)] if system_instruction else prompt
        return self._get_llm().invoke(messages).content

    def get_agent_executor(self, tools, system_instruction=None, verbose=False):
        return create_agent(
            model=self._get_llm(),
            tools=tools,
            system_prompt=system_instruction,
            debug=verbose,
        )
