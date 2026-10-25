import os
from dotenv import load_dotenv
from ai_core.providers.openai_provider import OpenAIProvider

load_dotenv()

_PROVIDER_REGISTRY = {
    "openai": OpenAIProvider,
}


def get_llm_client(provider=None, model=None, api_key=None, **kwargs):
    provider_name = (provider or os.getenv("LLM_PROVIDER", "openai")).lower()
    provider_cls = _PROVIDER_REGISTRY.get(provider_name)
    if not provider_cls:
        available = ", ".join(_PROVIDER_REGISTRY.keys())
        raise ValueError(
            f"Unsupported LLM provider: '{provider_name}'. Currently configured providers: {available}"
        )

    return provider_cls(model=model, api_key=api_key, **kwargs)
