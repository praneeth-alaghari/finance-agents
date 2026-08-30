import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ai_core.providers.base import BaseLLMProvider

# Ensure environment variables are loaded from .env
load_dotenv()


class OpenAIProvider(BaseLLMProvider):
    """LangChain-powered LLM Provider for OpenAI using native model defaults."""

    def __init__(self, model=None, api_key=None, temperature=None, **kwargs):
        load_dotenv(override=True)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        self._extra_kwargs = kwargs
        self._llm = None

    def _get_llm(self):
        """Lazy-loads ChatOpenAI without forcing a temperature parameter."""
        if self._llm is None:
            if not self.api_key or self.api_key == "your_openai_api_key_here":
                raise ValueError(
                    "OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file."
                )

            llm_kwargs = dict(self._extra_kwargs)
            # Only specify temperature if explicitly requested by the caller
            if self.temperature is not None:
                llm_kwargs["temperature"] = self.temperature

            # Accommodate deep reasoning models (o1, o3, etc.) that take longer to think
            if "timeout" not in llm_kwargs and "request_timeout" not in llm_kwargs:
                llm_kwargs["timeout"] = 120.0

            self._llm = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                **llm_kwargs,
            )
        return self._llm

    def generate(self, prompt, system_instruction=None, temperature=None):
        """Generates text completion using native model defaults."""
        if not prompt or not str(prompt).strip():
            raise ValueError("Prompt cannot be empty.")

        llm = self._get_llm()

        messages = []
        if system_instruction:
            messages.append(SystemMessage(content=system_instruction))
        messages.append(HumanMessage(content=prompt))

        # Only override temperature if explicitly passed
        if temperature is not None:
            llm = llm.bind(temperature=temperature)

        response = llm.invoke(messages)
        return response.content

    def get_chat_model(self):
        """Returns the raw LangChain BaseChatModel instance for agent graphs/chains."""
        return self._get_llm()
