import streamlit as st

# Função para mostrar o formulário de usuário e senha baseado na seleção do modelo
def exibir_campos_usuario_senha(modelo):
    if modelo == 'AWS':
        usuario = st.text_input("ACCESS KEY")
        senha = st.text_input("SECRET KEY", type="password")
        return usuario, senha
    else:
        st.write("Solução em construção...")
        return None, None

# Cabeçalho
st.title("Verificação de Documentos")

# Campo 0 - Formulário variável com os subcampos
modelo = st.selectbox(
    "Modelo utilizado",
    ("AWS", "GCP", "AZURE")
)

usuario, senha = exibir_campos_usuario_senha(modelo)

# Campo 1 - Enviar documento (RG ou CNH)
st.header("Envie seu documento (RG ou CNH com menor área de fundo possível)")
documento = st.file_uploader("Escolha uma imagem do seu documento", type=["jpg", "jpeg", "png"])

# Campo 2 - Tirar uma foto sua
st.header("Tire uma foto sua!")
camera_enabled = st.session_state.get('camera_enabled', False)  # Verifica se a câmera está ativada ou não

# Botão para ativar/desativar a câmera
if st.button("Ativar/Desativar Câmera"):
    camera_enabled = not camera_enabled
    st.session_state['camera_enabled'] = camera_enabled

# Exibe a entrada da câmera se ativada
foto_usuario = None
if camera_enabled:
    foto_usuario = st.camera_input("Tire sua foto")

# Campo 3 - Enviar comprovante de residência
st.header("Envie um comprovante de residência")
comprovante_residencia = st.file_uploader("Escolha uma imagem do seu comprovante de residência", type=["jpg", "jpeg", "png"])

# Botão de verificação
if st.button("Verificar documentos!"):
    # Verificação simples para garantir que todos os campos foram preenchidos
    if modelo and documento and foto_usuario and comprovante_residencia:
        if modelo == 'AWS' and usuario and senha:
            st.success("Documentos verificados com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos e/ou selecione um modelo disponível antes de enviar.")
    else:
        st.error("Por favor, preencha todos os campos e/ou selecione um modelo disponível antes de enviar.")
