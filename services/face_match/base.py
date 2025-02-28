from abc import ABC, abstractmethod


class FaceMatchBase(ABC):
    @abstractmethod
    def match_faces(self, binary_image1: bytes, binary_image2: bytes) -> dict:
        pass
