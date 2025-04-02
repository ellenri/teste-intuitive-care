import pandas as pd
import numpy as np
import psycopg2
import logging
import os
from dotenv import load_dotenv

# Configuração do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def importar_dados_csv_para_postgres_pandas(conn, caminho_arquivo_csv, nome_tabela):
    """Importa dados de um arquivo CSV para uma tabela PostgreSQL usando pandas."""

    cursor = conn.cursor()

    try:
        # Ler a query de criação da tabela do arquivo
        with open('../sql_scripts/criar_tabela_operadoras.sql', 'r') as arquivo_sql:
            query_criar_tabela = arquivo_sql.read()

        cursor.execute(query_criar_tabela)
        conn.commit()
        print("Tabela 'operadoras' criada com sucesso.")

        # Ler o arquivo CSV usando pandas
        df = pd.read_csv(caminho_arquivo_csv, sep=';', encoding='utf-8')

        # Converter nomes das colunas para minúsculas e remover espaços extras
        df.columns = [col.lower().strip() for col in df.columns]

        # Criar a query de inserção com base nos nomes das colunas
        colunas = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        query_insercao = f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({placeholders})"

        # Converter valores NaN para None (NULL em PostgreSQL)
        df = df.where(pd.notnull(df), None)
        df = df.replace({np.nan: None})

        # Converter a coluna para datetime, tratando erros e NaT
        df['data_registro_ans'] = pd.to_datetime(df['data_registro_ans'], errors='coerce')
        df['data_registro_ans'] = df['data_registro_ans'].replace({pd.NaT: None})

        # Inserir os dados linha por linha
        for _, row in df.iterrows():
            try:

                cursor.execute(query_insercao, tuple(row))
                # else:
                #     print(f"Aviso: CNPJ duplicado encontrado: {row['cnpj']}")
            except psycopg2.Error as e:
                logging.error(f"Erro ao inserir dados: {e}")
                print(cursor.query)
                # print(f"Erro ao inserir linha: {row}")
                print(f"Erro: {e}")

        conn.commit()
        print(f"Dados importados com sucesso para a tabela {nome_tabela}.")

    except (psycopg2.Error, FileNotFoundError, pd.errors.ParserError) as e:
        conn.rollback()
        print(f"Erro ao importar dados: {e}")

    finally:
        cursor.close()

