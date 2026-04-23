import requests
import os
from datetime import datetime

URL_BASE = "https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/shpc/dsan"

FORMATOS = {
    2026: "{mes:02d}-dados-abertos-precos-diesel-gnv.csv", 
    2025: "precos-diesel-gnv-{mes:02d}.csv"
}


def download_file(url, filename):
    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status() 
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Sucesso: {filename}")
    except Exception as e:
        print(f"Arquivo não baixado {filename}: {e}")

for ano, formato in FORMATOS.items():
    print(f"\nIniciando downloads de {ano}...")
    mes_limite = datetime.now().month if ano == datetime.now().year else 13
    for mes in range(1, mes_limite):
        name_archive = formato.format(mes=mes)
        url_end = f"{URL_BASE}/{ano}/{name_archive}"
        
        os.makedirs(os.path.join('./data', str(ano)), exist_ok=True)
        save_path = os.path.join('./data', str(ano), name_archive)
        
        download_file(url_end, save_path)