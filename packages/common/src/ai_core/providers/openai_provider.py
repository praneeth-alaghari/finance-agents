import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ai_core.providers.base import BaseLLMProvider

# Ensure environment variables are loaded from .env
load_dotenv()


class OpenAIProvider(BaseLLMProvider):
    """LangChain-powered LLM Provider for OpenAI."""

    def __init__(self, model=None, api_key=None, temperature=0.7, **kwargs):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        self._extra_kwargs = kwargs
        self._llm = None

    def _get_llm(self):
        """Lazy-loads the ChatOpenAI client with credential verification."""
        if self._llm is None:
            if not self.api_key or self.api_key == "your_openai_api_key_here":
                raise ValueError(
                    "OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file."
                )
            self._llm = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                temperature=self.temperature,
                **self._extra_kwargs,
            )
        return self._llm

    def generate(self, prompt, system_instruction=None, temperature=None):
        """Generates text completion using LangChain ChatOpenAI."""
        if not prompt or not str(prompt).strip():
            raise ValueError("Prompt cannot be empty.")

        llm = self._get_llm()

        messages = []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        messages.append(HumanMessage(content=prompt))

        if temperature is not None:
            llm = llm.bind(temperature=temperature)

        response = llm.invoke(messages)
        return response.content

    def get_chat_model(self):
        """Returns the raw LangChain BaseChatModel instance for agent graphs/chains."""
        return self._get_llm()
