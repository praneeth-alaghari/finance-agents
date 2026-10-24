import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from ai_core.providers.base import BaseLLMProvider

# Ensure environment variables are loaded from .env
load_dotenv()


class _AgentRunnableWrapper:
    """Adapts a compiled tool-calling graph to support .invoke({'input': ...})."""

    def __init__(self, graph):
        self._graph = graph

    def invoke(self, inputs):
        prompt_text = inputs.get("input") if isinstance(inputs, dict) else inputs
        if isinstance(prompt_text, str):
            messages = [("user", prompt_text)]
        else:
            messages = prompt_text
        res = self._graph.invoke({"messages": messages})
        last_message = res["messages"][-1]
        output = last_message.content if hasattr(last_message, "content") else str(last_message)
        return {"output": output, "messages": res.get("messages", [])}


class OpenAIProvider(BaseLLMProvider):
    """LangChain-powered LLM Provider for OpenAI using native model defaults."""

    def __init__(self, model=None, api_key=None, temperature=None, **kwargs):
        load_dotenv(override=True)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.temperature = temperature
        self._extra_kwargs = kwargs
        self._llm = None
        self._tool_llm = None

    def _get_llm(self, for_tools=False):
        """Lazy-loads ChatOpenAI without forcing a temperature parameter."""
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            raise ValueError(
                "OpenAI API key is not configured. Please set OPENAI_API_KEY in your .env file."
            )

        if for_tools:
            if self._tool_llm is None:
                llm_kwargs = dict(self._extra_kwargs)
                if "timeout" not in llm_kwargs and "request_timeout" not in llm_kwargs:
                    llm_kwargs["timeout"] = 120.0
                if any(k in (self.model or "").lower() for k in ["luna", "o1", "o3", "reasoning"]):
                    llm_kwargs["reasoning_effort"] = "none"
                self._tool_llm = ChatOpenAI(
                    model=self.model,
                    api_key=self.api_key,
                    **llm_kwargs,
                )
            return self._tool_llm

        if self._llm is None:
            llm_kwargs = dict(self._extra_kwargs)
            if self.temperature is not None:
                llm_kwargs["temperature"] = self.temperature
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

        if temperature is not None:
            llm = llm.bind(temperature=temperature)

        response = llm.invoke(messages)
        return response.content

    def get_chat_model(self):
        """Returns the raw LangChain BaseChatModel instance for agent graphs/chains."""
        return self._get_llm()

    def get_agent_executor(self, tools, system_instruction=None, verbose=False):
        """Builds and returns a native tool-calling agent wired with the given tools.

        Uses native function calling with the given tools, handling reasoning models
        seamlessly and returning an invokable wrapper compatible with AgentExecutor syntax.
        """
        llm = self._get_llm(for_tools=True)
        graph = create_react_agent(
            model=llm,
            tools=tools,
            prompt=system_instruction,
        )
        return _AgentRunnableWrapper(graph)
