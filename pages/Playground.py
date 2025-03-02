from services.llm.gpt import GptTextInterpreter
from services.face_match.aws_rekognition import AwsRekognitionFaceMatch
from services.face_extract.aws_rekognition import AwsRekognitionFaceExtract
from services.text_extract.aws_textract import AwsTextract

import streamlit as st
from boto3 import client as aws_client
from openai import OpenAI


st.write("# Playground")
st.write('## Modelos')
st.write("Escolha quais modelos vão avaliar os documentos")
col1, col2, col3, col4 = st.columns(4)

with col1:
    model_img_to_text = st.selectbox(
        "Imagem para texto",
        ("AWS", "Azure (em breve)", "GCP (em breve)")
    )
with col2:
    model_llm = st.selectbox(
        "Interpretação de texto",
        ("OpenAI", "Azure (em breve)", "AWS (em breve)", "GCP (em breve)")
    )
with col3:
    model_face_extract = st.selectbox(
        "Identificador de rosto",
        ("AWS", "Azure (em breve)", "GCP (em breve)")
    )
with col4:
    model_face_match = st.selectbox(
        "Comparador de rosto",
        ("AWS", "Azure (em breve)", "GCP (em breve)")
    )

with st.sidebar:
    st.write("## AWS")
    aws_access_key = st.text_input("ACCESS KEYS")
    aws_secret_key = st.text_input("SECRET KEY", type="password")

with st.sidebar:
    st.write("## OpenAI")
    openai_api_key = st.text_input("API KEY", type="password")

all_services = {
    "model_img_to_text":
        {
            "AWS":
                {
                    "obj": AwsTextract,
                    "client_obj": aws_client,
                    "client_kwargs": {
                        "service_name": "textract",
                        "aws_access_key_id": aws_access_key,
                        "aws_secret_access_key": aws_secret_key,
                        "region_name": "us-east-1"
                    }
                },
        },
    "model_llm":
        {
            "OpenAI":
                {
                    "obj": GptTextInterpreter,
                    "client_obj": OpenAI,
                    "client_kwargs": {
                        "api_key": openai_api_key,
                    }
                }
        },
    "model_face_extract":
        {
            "AWS":
                {
                    "obj": AwsRekognitionFaceExtract,
                    "client_obj": aws_client,
                    "client_kwargs": {
                        "service_name": "rekognition",
                        "aws_access_key_id": aws_access_key,
                        "aws_secret_access_key": aws_secret_key,
                        "region_name": "us-east-1"
                    }
                }
        },
    "model_face_match":
        {
            "AWS":
                {
                    "obj": AwsRekognitionFaceMatch,
                    "client_obj": aws_client,
                    "client_kwargs": {
                        "service_name": "rekognition",
                        "aws_access_key_id": aws_access_key,
                        "aws_secret_access_key": aws_secret_key,
                        "region_name": "us-east-1"
                    }
                }
        }
}

clients = {
    "AWS": aws_client
}


st.write('## Documentos')
st.write("Envie os arquivos a seguir para verificarmos sua identidade")

st.write("📄 **Envie seu documento (RG ou CNH)**")
document_file_input = st.file_uploader("Envie um arquivo de um documento com CPF e foto:",type=["jpg", "jpeg", "png"])

st.write("🏠 **Envie uma foto de um comprovante de residência**")
address_document_input = st.file_uploader("A conta deve conter seu nome e endereço", type=["jpg", "jpeg", "png", "pdf"])

st.write("📸 **Tire uma foto sua!**")
st.write("Tire uma foto sem outras pessoas ao seu lado")
camera_enabled = st.session_state.get('camera_enabled', False)

if st.button("Ligar/Desligar Câmera"):
    camera_enabled = not camera_enabled
    st.session_state['camera_enabled'] = camera_enabled

user_photo_input = None
if camera_enabled:
    user_photo_input = st.camera_input("Tire sua foto")

if st.button("Verificar identidade!"):

    model_img_to_text_obj = all_services["model_img_to_text"].get(model_img_to_text)
    model_llm_obj = all_services["model_llm"].get(model_llm)
    model_face_extract_obj = all_services["model_face_extract"].get(model_face_extract)
    model_face_match_obj = all_services["model_face_match"].get(model_face_match)

    if model_img_to_text_obj and model_llm_obj and model_face_extract_obj and model_face_match_obj:
        if user_photo_input and address_document_input and document_file_input:
            user_photo = user_photo_input.read()
            address_document = address_document_input.read()
            document_file = document_file_input.read()
            st.toast("Extraindo informações de registro...")
            try:
                model_img_to_text_service = model_img_to_text_obj['obj'](
                    model_img_to_text_obj['client_obj'](
                        **model_img_to_text_obj['client_kwargs']
                    )
                )
                document_file_user_data = model_img_to_text_service.extract_text(document_file)
                address_document_user_data = model_img_to_text_service.extract_text(address_document)
                st.toast("Documentos convertidos em texto!")
            except Exception as e:
                st.error(f'Não foi possível transformar o modelo de Imagem para texto. Segue erro: {e}')
                raise Exception(e)



            st.toast("Extraindo dados relevantes...")
            try:
                model_llm_service = model_llm_obj['obj'](
                    model_llm_obj['client_obj'](
                        **model_llm_obj['client_kwargs']
                    )
                )
                name_and_cpf = (
                    model_llm_service
                    .interpret_text_extraction(
                        ocr_text=document_file_user_data,
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": "identificacao_cnh_rg",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "nome": {
                                            "description": "O nome completo da pessoa conforme identificado na CNH ou RG apenas em letras minusculas. Se não for encontrado, retorne null.",
                                            "type": ["string", "null"],
                                            "nullable": True
                                        },
                                        "cpf": {
                                            "description": "O CPF da pessoa conforme identificado na CNH ou RG, apenas números. Se não for encontrado, retorne null.",
                                            "type": ["string", "null"],
                                            "pattern": "^[0-9]{11}$",
                                            "nullable": True
                                        }
                                    },
                                    "required": ["nome", "cpf"],
                                    "additionalProperties": False
                                }
                            }
                        }
                        )
                )
                name_and_address = (
                    model_llm_service
                    .interpret_text_extraction(
                        ocr_text=address_document_user_data,
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": "identificacao_comprovante_residencia",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "nome": {
                                            "description": "O nome completo da pessoa que deverá pagar a conta, apenas em letras minusculas. Se não for encontrado, retorne null.",
                                            "type": ["string", "null"],
                                            "nullable": True
                                        },
                                        "endereco": {
                                            "description": "O endereço completo da pessoa que deverá pagar a conta. Se não for encontrado, retorne null.",
                                            "type": ["string", "null"],
                                            "nullable": True
                                        }
                                    },
                                    "required": ["nome", "cpf"],
                                    "additionalProperties": False
                                }
                            }
                        }
                        )
                )
                if not name_and_cpf['nome']:
                    raise Exception("Não foi possível extrair o nome do documento de identidade")
                if not name_and_cpf['cpf']:
                    raise Exception("Não foi possível extrair o CPF do documento de identidade")
                if not name_and_address['nome']:
                    raise Exception("Não foi possível extrair o nome do comprovante de residência")
                if not name_and_address['endereco']:
                    raise Exception("Não foi possível extrair o endereco do documento de residencia")

                st.toast("Nome, CPF e Endereço identificados")
                if name_and_cpf['nome'] != name_and_address['nome']:
                    raise Exception(f"Nomes não estão iguais nos documentos! Nome do documento = {name_and_cpf['nome']} e Nome do comprovante = {name_and_address['nome']}")
                st.toast("Documentos com nomes corretos!")
            except Exception as e:
                st.error(f'Não foi possível identificar os dados do usuário. Segue erro: {e}')
                raise Exception(e)


            st.toast("Extraindo rosto...")
            try:
                model_face_extract_service = model_face_extract_obj['obj'](
                    model_face_extract_obj['client_obj'](
                        **model_face_extract_obj['client_kwargs']
                    )
                )
                document_face = model_face_extract_service.extract_faces(
                    binary_image=document_file
                )
                st.toast("Rosto encontrado!")
            except Exception as e:
                st.error(f'Não foi possível extrair o rosto do usuário. Segue erro:{e}')
                raise Exception(e)



            st.toast("Comparando identidade e foto...")
            try:
                model_face_match_service = model_face_match_obj['obj'](
                    model_face_match_obj['client_obj'](
                        **model_face_match_obj['client_kwargs']
                    )
                )

                face_match = model_face_match_service.match_faces(
                    binary_image1=document_face,
                    binary_image2=user_photo
                )
                st.toast("Identidades correspondem!")
            except Exception as e:
                st.error(f'O usuário da foto não é o mesmo do documento. Segue erro: {e}')
                raise Exception(e)


            st.toast("Documentos validados!", icon="😊")
            st.markdown(f"""
                ## Resultados:
                A partir do texto extraído do documento de identidade, foram identificados os seguintes dados:\n
                **Nome**: {name_and_cpf['nome']}\n
                **CPF**: {name_and_cpf['cpf']}\n
                A partir do texto extraído do comprovante de renda, foram identificados os seguintes dados:\n
                **Nome**: {name_and_address['nome']}\n
                **Endereço**: {name_and_address['endereco']}\n
                O rosto do documento de identidade e da foto tirada correspondem a mesma pessoa, com um nível
                de similaridade de {face_match['similarity']}.
            """)
        else:
            st.toast("Faça o upload de todos os documentos necessários!", icon="⚠️")
            st.error("Faça o upload de todos os documentos necessários!")


    else:
        st.toast("Um dos modelos ainda não foi implementado", icon="😢")
        st.error("Verifique se todos os modelos escolhidos já foram implementados")
