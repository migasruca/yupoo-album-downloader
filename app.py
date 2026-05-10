import streamlit as st
import requests
from bs4 import BeautifulSoup
import zipfile
import io

st.set_page_config(page_title="Yupoo Downloader", layout="wide")

st.title("📦 Yupoo Album Downloader")
st.write("Insira o link de um álbum do Yupoo para visualizar e baixar todas as imagens.")

url = st.text_input("Link do álbum Yupoo:")

if st.button("Procurar Imagens"):
    if url:
        try:
            with st.spinner("A procurar imagens..."):
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                    "Referer": "https://yupoo.com/"
                }
                
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                
                images = []
                for img in soup.find_all('img'):
                    src = img.get('data-origin-src') or img.get('data-src') or img.get('src')
                    if src and not src.startswith('data:image'):
                        if src.startswith('//'):
                            src = 'https:' + src
                        images.append(src)
                
            if images:
                st.success(f"Encontradas {len(images)} imagens!")
                
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for i, img_url in enumerate(images):
                        try:
                            img_data = requests.get(img_url, headers=headers).content
                            zip_file.writestr(f"imagem_{i+1}.jpg", img_data)
                        except:
                            continue
                
                st.download_button(
                    label="⬇️ Baixar Todas as Imagens (.ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name="yupoo_album.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                
                st.divider()
                cols = st.columns(4)
                for idx, img_url in enumerate(images):
                    with cols[idx % 4]:
                        st.image(img_url, use_container_width=True)
            else:
                st.warning("Nenhuma imagem encontrada.")
        except Exception as e:
            st.error(f"Erro: {e}")
