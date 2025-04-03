import logging
import os
import glob
import zipfile
from datetime import datetime
from urllib.parse import urljoin
import pandas as pd
import requests
from bs4 import BeautifulSoup


from web_scraping_transformacao_dados.baixar_anexo import baixar_anexo

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


diretorio_origem = os.path.join("../../../output/demonstracoes_contabeis")
diretorio_destino = os.path.join("../../output", "demonstracoes_contabeis", "extraido")


def baixar_demonstracoes_contabeis(url_base, diretorio_download):
    ano_atual = datetime.now().year
    anos = [ano_atual - 2, ano_atual - 1]

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


def extrair_arquivos_zip(diretorio_origem, diretorio_destino):

    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)
        print(f"Criado diretório de destino: {diretorio_destino}")

    zip_files = glob.glob(os.path.join(diretorio_origem, '*.zip'))
    if not zip_files:
        print("Nenhum arquivo ZIP encontrado no diretório de origem.")
        return

    for zip_file in zip_files:
        try:
            with zipfile.ZipFile(zip_file, 'r') as z:
                z.extractall(diretorio_destino)
                print(f"Extraído: {zip_file} para {diretorio_destino}")
        except Exception as e:
            print(f"Erro ao extrair {zip_file}: {e}")

def ler_e_concatenar_csv(diretorio_destino):
    arquivos_csv = glob.glob(os.path.join(diretorio_destino, '*.csv'))
    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado.")
        return None

    lista_dfs = []
    for arquivo in arquivos_csv:
        try:
            df = pd.read_csv(arquivo, sep=';', encoding='utf-8')
            lista_dfs.append(df)
            print(f"Lido {arquivo} com {len(df)} registros.")
        except Exception as e:
            print(f"Erro ao ler {arquivo}: {e}")

    if lista_dfs:
        df_concatenado = pd.concat(lista_dfs, ignore_index=True)
        return df_concatenado
    return None


def criar_tabela_unica(conn, tabela):
    cursor = conn.cursor()
    try:
        with open('../sql_scripts/criar_tabela_demonstracao_contabil.sql', 'r') as file:
            query_criar_tabela_contabil = file.read()
        query = query_criar_tabela_contabil.format(tabela=tabela)
        cursor.execute(query)
        conn.commit()
        print(f"Tabela '{tabela}' criada com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar a tabela: {e}")
    finally:
        cursor.close()


def importar_dados(conn, tabela, df):
    cursor = conn.cursor()
    df.columns = [col.lower().strip() for col in df.columns]
    df = df.where(pd.notnull(df), None)

    colunas = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    query_insert = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"

    try:
        for _, row in df.iterrows():
            cursor.execute(query_insert, tuple(row))
            print(row)
        conn.commit()
        print("Dados importados com sucesso!")
    except Exception as e:
        conn.rollback()
        print(cursor.query)
        print(row)
        print("Erro ao importar dados:", e)
    finally:
        cursor.close()
        conn.close()
        print("Conexão com o banco de dados fechada.")