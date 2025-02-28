from abc import ABC, abstractmethod


class FaceExtractBase(ABC):
    @abstractmethod
    def extract_faces(self, binary_image: bytes) -> bytes:
        pass

