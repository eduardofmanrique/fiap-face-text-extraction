import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.write("# 🔍 Validador de documentos")

st.markdown(
    """
    ## Sobre
    O projeto a seguir foi realizado para a matéria de Cognitive Enviroments do curso
    de MBA em Data Science & AI da FIAP. \n
    A ideia é um playground que testa modelos diferentes para validar a identidade
    de um suposto usuário que deseja fraudar a contratação de serviços financeiros. \n
    Por enquanto, estamos utilizando serviços de API da **AWS** (Rekognition e Textract) e 
    **OpenAI**. Porém, o desenvolvimento da aplicação permite adicionar facilmente
    novos provedores para comparar a eficácia de serviços de cloud de Computer Vision e LLM.\n

    ## Requisitos para uso
    Para testar os modelos, é necessário credenciais de acesso com permissões aos serviços.\n
    **🔑 AWS**\n
    Necessário access e secret keys com as políticas AmazonRekognitionFullAccess e AmazonTextractFullAccess\n
    [Documentação AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) \n
    **🔑 OpenAI**\n
    Necessário chave de API com permissões de recurso Model = Read e Model capabilities = Write \n
    [Documentação OpenAI](https://platform.openai.com/api-keys)
    """
)
