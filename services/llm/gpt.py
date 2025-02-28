from services.llm.base import LlmTextInterpreterBase
from openai import OpenAI
import json


class GptTextInterpreter(LlmTextInterpreterBase):
    def __init__(self, client: OpenAI):
        self.client = client

    def interpret_text_extraction(self,
                                  ocr_text: str,
                                  response_format: dict) -> dict:

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "developer", "content": "Você extrai dados de identificação gerados por OCR de acordo com o json de resposta solicitado."},
                {"role": "user", "content": f"Segue o texto extraido por ocr: '{ocr_text}'. Retorne os parametros de acordo com a descrição"}
            ],
            response_format=response_format
        )

        try:
            return json.loads(response.choices[0].message.content.strip())
        except:
            return {"nome": None, "cpf": None}
