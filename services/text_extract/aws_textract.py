from services.text_extract.base import TextExtractBase
import boto3


class AwsTextract(TextExtractBase):
    def __init__(self,
                 client: boto3.client
                 ):
        self.textract_client = client

    def extract_text(self, binary_image: bytes) -> str:
        response = self.textract_client.detect_document_text(
            Document={"Bytes": binary_image}
        )
        texts = [b.get('Text') for b in response['Blocks'] if b['BlockType']=='LINE']
        if len(texts) == 0:
            raise Exception("Não foi encontrado nenhum texto na imagem!")
        return " ".join(texts)
