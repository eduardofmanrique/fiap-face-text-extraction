# Trabalho Final - Cognitive Environments - FIAP
## Sobre
O projeto a seguir foi realizado para a matéria de Cognitive Enviroments do curso
de MBA em Data Science & AI da FIAP.
A ideia é um playground que testa modelos diferentes para validar a identidade
de um suposto usuário que deseja fraudar a contratação de serviços financeiros. 
Por enquanto, estamos utilizando serviços de API da **AWS** (Rekognition e Textract) e 
**OpenAI**. Porém, o desenvolvimento da aplicação permite adicionar facilmente
novos provedores para comparar a eficácia de serviços de cloud de Computer Vision e LLM.

## Requisitos para uso
Para testar os modelos, é necessário credenciais de acesso com permissões aos serviços.<br />
**🔑 AWS**<br />
Necessário access e secret keys com as políticas AmazonRekognitionFullAccess e AmazonTextractFullAccess<br />
[Documentação AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)<br />
**🔑 OpenAI**<br />
Necessário chave de API com permissões de recurso Model = Read e Model capabilities = Write<br />
[Documentação OpenAI](https://platform.openai.com/api-keys)

## Como usar
Acessar a página https://fiap-document-validator-cognitive-environments.streamlit.app/ <br >
No menu lateral, selecionar "Playground". <br >
Preenhcer as credenciais das APIs no menu lateral. <br >
Escolher os modelos desejados. <br >
Fazer o upload de todos os arquivos necessários. <br >
Apertar o botão "Verificar Identidade!" e aguardar os resultados
