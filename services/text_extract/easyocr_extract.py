from services.text_extract.base import TextExtractBase
import easyocr
import numpy as np
import cv2

class EasyOCRTextExtract(TextExtractBase):
    def __init__(self, reader = easyocr.Reader):
        self.reader = reader

    def extract_text(self, binary_image: bytes) -> str:

        nparr = np.frombuffer(binary_image, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        results = self.reader.readtext(image, detail=0)

        if not results:
            raise Exception("Não foi encontrado nenhum texto na imagem!")

        return " ".join(results)
