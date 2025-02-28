import boto3
from services.face_match.base import FaceMatchBase


class AwsRekognitionFaceMatch(FaceMatchBase):
    def __init__(self, client: boto3.client):
        self.rekognition_client = client

    def match_faces(self, binary_image1: bytes, binary_image2: bytes) -> dict:
        response = self.rekognition_client.compare_faces(
            SourceImage={"Bytes": binary_image1},
            TargetImage={"Bytes": binary_image2},
            SimilarityThreshold=80
        )

        if len(response['FaceMatches']) == 0:
            raise Exception('Não foi encontrada nenhuma foto similar!')

        face_match = response['FaceMatches'][0]
        similarity = face_match['Similarity']

        return {
            "similarity": similarity
        }
