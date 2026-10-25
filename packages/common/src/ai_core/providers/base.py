from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt, system_instruction=None, **kwargs):
        pass

    @abstractmethod
    def get_agent_executor(self, tools, system_instruction=None, verbose=False):
        pass
