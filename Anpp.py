import requests

def download_yupoo_img(url):
    headers = {
        "Referer": "https://yupoo.com/", # Essencial para o Yupoo permitir o acesso
        "User-Agent": "Mozilla/5.0..."
    }
    response = requests.get(url, headers=headers)
    return response.content
