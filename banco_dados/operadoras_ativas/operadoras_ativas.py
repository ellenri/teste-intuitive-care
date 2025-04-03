from urllib.parse import urljoin

import pandas as pd
import numpy as np
import psycopg2
import logging
import os

import requests


from web_scraping_transformacao_dados.baixar_anexo import baixar_anexo

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def baixar_relatorio_operadoras_ativas(url_operadoras_ativas_ans, diretorio_download):
    url_arquivo = urljoin(url_operadoras_ativas_ans, 'Relatorio_cadop.csv')
    nome_arquivo = os.path.join(diretorio_download, 'Relatorio_cadop.csv')

    try:
        baixar_anexo(url_arquivo, nome_arquivo)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar {url_arquivo}: {e}")

def importar_dados(conn, caminho_arquivo_csv, nome_tabela):

    cursor = conn.cursor()

    try:
        with open('../output/sql_scripts/criar_tabela_operadoras.sql', 'r') as arquivo_sql:
            query_criar_tabela = arquivo_sql.read()

        cursor.execute(query_criar_tabela)
        conn.commit()
        print("Tabela 'operadoras' criada com sucesso.")


        df = pd.read_csv(caminho_arquivo_csv, sep=';', encoding='utf-8')

        df.columns = [col.lower().strip() for col in df.columns]

        colunas = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        query_insercao = f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({placeholders})"

        df = df.where(pd.notnull(df), None)
        df = df.replace({np.nan: None})

        df['data_registro_ans'] = pd.to_datetime(df['data_registro_ans'], errors='coerce')
        df['data_registro_ans'] = df['data_registro_ans'].replace({pd.NaT: None})

        for _, row in df.iterrows():
            try:
                cursor.execute(query_insercao, tuple(row))

            except psycopg2.Error as e:
                logging.error(f"Erro ao inserir dados: {e}")
                print(f"Erro: {e}")

        conn.commit()
        print(f"Dados importados com sucesso para a tabela {nome_tabela}.")

    except (psycopg2.Error, FileNotFoundError, pd.errors.ParserError) as e:
        conn.rollback()
        print(f"Erro ao importar dados: {e}")

    finally:
        cursor.close()

