import streamlit as st
import requests
from bs4 import BeautifulSoup
import zipfile
import io

st.set_page_config(page_title="Yupoo Album Downloader", layout="wide")

st.title("📦 Yupoo Album Downloader Pro")

url = st.text_input("Link do álbum Yupoo:")

# Headers mais robustos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Referer": "https://yupoo.com/"
}

if st.button("🚀 Extrair Álbum"):
    if url:
        try:
            with st.spinner("A extrair imagens..."):
                res = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(res.content, "html.parser")
                
                # Procura as imagens especificamente nas divs da galeria
                images = []
                for img in soup.find_all('img'):
                    # O Yupoo guarda a imagem real em data-origin-src ou data-src
                    src = img.get('data-origin-src') or img.get('data-src') or img.get('src')
                    if src and "logo" not in src.lower() and not src.startswith('data:image'):
                        if src.startswith('//'): src = 'https:' + src
                        images.append(src)
                
                # Remover duplicados mantendo a ordem
                images = list(dict.fromkeys(images))

            if images:
                st.success(f"Encontradas {len(images)} imagens!")
                
                zip_buffer = io.BytesIO()
                valid_images_count = 0
                
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    cols = st.columns(4)
                    
                    for i, img_url in enumerate(images):
                        try:
                            img_res = requests.get(img_url, headers=HEADERS, timeout=10)
                            if img_res.status_code == 200:
                                img_data = img_res.content
                                # Adiciona ao ZIP
                                zip_file.writestr(f"foto_{i+1}.jpg", img_data)
                                valid_images_count += 1
                                
                                # Mostra na interface
                                with cols[i % 4]:
                                    st.image(img_data, use_container_width=True)
                        except:
                            continue
                
                if valid_images_count > 0:
                    st.divider()
                    st.download_button(
                        label=f"⬇️ BAIXAR {valid_images_count} FOTOS (.ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name="album_yupoo.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
            else:
                st.warning("Não foram encontradas imagens. Tente atualizar a página.")
                
        except Exception as e:
            st.error(f"Erro ao aceder ao álbum: {e}")
