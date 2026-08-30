from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Abstract base class establishing the contract for all LLM providers."""

    @abstractmethod
    def generate(self, prompt, system_instruction=None, temperature=None):
        """Generates text from the LLM given a prompt and optional system instructions."""
        pass
