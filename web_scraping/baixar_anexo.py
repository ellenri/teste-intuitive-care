import multiprocessing
import os
from datetime import datetime

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

def baixar_demonstracoes_contabeis(url_base, diretorio_download):
    ano_atual = datetime.now().year
    anos = [ano_atual - 2, ano_atual - 1]  # Últimos 2 anos

    # Verificar quais anos existem no repositório
    anos_existentes = []
    for ano in anos:
        url_ano = urljoin(url_base, str(ano) + '/')
        try:
            response = requests.get(url_ano)
            response.raise_for_status()
            anos_existentes.append(ano)
        except requests.exceptions.HTTPError:
            print(f"Diretório {ano} não encontrado. Pulando.")

    for ano in anos_existentes:
        url_ano = urljoin(url_base, str(ano) + '/')
        response = requests.get(url_ano)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        links_arquivos = soup.find_all('a', href=lambda href: href and (href.endswith('.zip') or href.endswith('.csv')))

        for link in links_arquivos:
            href = link['href']
            url_arquivo = urljoin(url_ano, href)
            nome_arquivo = os.path.join(diretorio_download, os.path.basename(href))

            try:
                baixar_anexo(url_arquivo, nome_arquivo)
            except requests.exceptions.RequestException as e:
                print(f"Erro ao baixar {url_arquivo}: {e}")\


def baixar_relatorio_cadop(url_operadoras_ativas_ans, diretorio_download):
    """Baixa o arquivo Relatorio_cadop.csv."""
    url_arquivo = urljoin(url_operadoras_ativas_ans, 'relatorio_cadop.csv')
    nome_arquivo = os.path.join(diretorio_download, 'relatorio_cadop.csv')

    try:
        baixar_anexo(url_arquivo, nome_arquivo)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {url_arquivo}: {e}")
