from abc import ABC, abstractmethod

class LlmTextInterpreterBase(ABC):
    @abstractmethod
    def interpret_text_extraction(self, **kwargs) -> dict:
        pass
