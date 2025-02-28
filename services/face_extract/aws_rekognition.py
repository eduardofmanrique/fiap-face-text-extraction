from services.face_extract.base import FaceExtractBase
import boto3
from PIL import Image
from io import BytesIO


class AwsRekognitionFaceExtract(FaceExtractBase):
    def __init__(self,
                 client: boto3.client
                 ):
        self.rekognition_client = client


    def extract_faces(self, binary_image: bytes) -> Image:
        # Detect faces in the image
        response = self.rekognition_client.detect_faces(
            Image={"Bytes": binary_image},
            Attributes=['ALL'],

        )

        if len(response['FaceDetails']) == 0 :
            raise Exception("Não foi encontrado nenhum rosto!")
        if len(response['FaceDetails']) > 1:
            raise Exception("Foi encontrado mais de um rosto!")

        face_details = response['FaceDetails'][0]

        if face_details['Confidence'] < 80:
            raise Exception(
                "Não foi encontrado nenhum rosto com índice de confiança maior que 80. Índice de confiança: {}".format(face_details['Confidence']))

        bounding_box = face_details['BoundingBox']
        img = Image.open(BytesIO(binary_image))
        width, height = img.size
        left = int(bounding_box['Left'] * width)
        top = int(bounding_box['Top'] * height)
        right = int((bounding_box['Left'] + bounding_box['Width']) * width)
        bottom = int((bounding_box['Top'] + bounding_box['Height']) * height)
        face_image = img.crop((left, top, right, bottom))
        img_bytesio = BytesIO()
        face_image.save(img_bytesio, format="PNG")
        img_bytesio.seek(0)
        return img_bytesio.getvalue()
