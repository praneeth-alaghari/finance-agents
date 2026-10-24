from ai_core.factory import get_llm_client
from ai_core.providers.base import BaseLLMProvider
from ai_core.providers.openai_provider import OpenAIProvider
from ai_core.tools.web_search import get_web_search_tool

# Alias for backward compatibility
LLMClient = OpenAIProvider

__all__ = [
    "get_llm_client",
    "BaseLLMProvider",
    "OpenAIProvider",
    "LLMClient",
    "get_web_search_tool",
]
