import multiprocessing
import os
import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def baixar_anexo(url_anexo, nome_arquivo):
    response = requests.get(url_anexo)
    response.raise_for_status()
    with open(nome_arquivo, 'wb') as f:
        f.write(response.content)
    print(f"Anexo baixado: {nome_arquivo}")

def baixar_anexos(url, diretorio_anexos):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    links_pdf = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

    tarefas = []
    anexos_baixados = []
    for link in links_pdf:
        href = link['href']
        if 'Anexo I' in link.text or 'Anexo II' in link.text:
            url_anexo = urljoin(url, href)
            nome_arquivo = os.path.join(diretorio_anexos, os.path.basename(href))
            tarefas.append((url_anexo, nome_arquivo))
            anexos_baixados.append(nome_arquivo)

    with multiprocessing.Pool() as pool:
        pool.starmap(baixar_anexo, tarefas)

    return anexos_baixados
