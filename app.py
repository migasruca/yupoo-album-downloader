import streamlit as st
import requests
from bs4 import BeautifulSoup
import zipfile
import io

# Configuração de estilo moderna
st.set_page_config(page_title="Yupoo Pro Downloader", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    .stDownloadButton>button { width: 100%; border-radius: 20px; background-color: #00c853; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Yupoo Album Downloader Pro")
st.write("Insira o link e baixe o álbum completo em segundos.")

url = st.text_input("Link do álbum Yupoo:", placeholder="https://dongshanstore.x.yupoo.com/albums/...")

# Cabeçalhos globais para enganar a proteção do Yupoo
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://yupoo.com/"
}

def get_image_bytes(img_url):
    try:
        response = requests.get(img_url, headers=HEADERS, timeout=10)
        return response.content
    except:
        return None

if st.button("🚀 Extrair Álbum"):
    if url:
        try:
            with st.spinner("A processar galeria..."):
                res = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(res.content, "html.parser")
                
                images = []
                # Captura os links reais das imagens
                for img in soup.find_all('img'):
                    src = img.get('data-origin-src') or img.get('data-src') or img.get('src')
                    if src and "logo" not in src.lower() and not src.startswith('data:image'):
                        if src.startswith('//'): src = 'https:' + src
                        images.append(src)
                
            if images:
                st.success(f"Encontradas {len(images)} imagens!")
                
                # Preparar o ZIP
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    
                    # Criar colunas para a grelha visual
                    cols = st.columns(4)
                    
                    for i, img_url in enumerate(images):
                        img_data = get_image_bytes(img_url)
                        if img_data:
                            # Adicionar ao ZIP
                            zip_file.writestr(f"foto_{i+1}.jpg", img_data)
                            
                            # Mostrar na interface (usando os bytes para evitar bloqueio)
                            with cols[i % 4]:
                                st.image(img_data, use_container_width=True, caption=f"Foto {i+1}")
                
                st.divider()
                st.download_button(
                    label="⬇️ BAIXAR TUDO AGORA (.ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="album_yupoo.zip",
                    mime="application/zip"
                )
            else:
                st.error("Não detetei fotos. Verifique se o link está correto.")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")

