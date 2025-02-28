from abc import ABC, abstractmethod


class TextExtractBase(ABC):
    @abstractmethod
    def extract_text(self, binary_image: bytes) -> dict:
        pass


