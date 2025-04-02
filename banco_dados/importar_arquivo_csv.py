import os
import glob
import zipfile

import pandas as pd
import psycopg2

from banco_dados.conexao import conectar_banco

diretorio_origem = os.path.join("output", "demonstracoes_contabeis")
diretorio_destino = os.path.join("output", "demonstracoes_contabeis", "extraido")


# def extrair_arquivos_zip(diretorio_origem, diretorio_destino):
#     """
#     Extrai todos os arquivos .zip do diretório_origem para o diretorio_destino.
#     Se o diretorio_destino não existir, ele será criado.
#     """
#     # Verifica se o diretório de destino existe, se não, cria.
#     if not os.path.exists(diretorio_destino):
#         os.makedirs(diretorio_destino)
#         print(f"Criado diretório de destino: {diretorio_destino}")
#
#     # Busca por todos os arquivos .zip no diretório de origem
#     zip_files = glob.glob(os.path.join(diretorio_origem, '*.zip'))
#     if not zip_files:
#         print("Nenhum arquivo ZIP encontrado no diretório de origem.")
#         return
#
#     for zip_file in zip_files:
#         try:
#             with zipfile.ZipFile(zip_file, 'r') as z:
#                 z.extractall(diretorio_destino)
#                 print(f"Extraído: {zip_file} para {diretorio_destino}")
#         except Exception as e:
#             print(f"Erro ao extrair {zip_file}: {e}")

def ler_e_concatenar_csv(diretorio):
    """
    Lê todos os arquivos CSV do diretório informado e retorna um único DataFrame concatenado.
    """
    arquivos_csv = glob.glob(os.path.join(diretorio, '*.csv'))
    if not arquivos_csv:
        print("Nenhum arquivo CSV encontrado.")
        return None

    lista_dfs = []
    for arquivo in arquivos_csv:
        try:
            # Ajuste o separador se necessário (ex.: sep=';' ou sep='\t')
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
    """
    Cria a tabela no PostgreSQL com a estrutura necessária.
    """
    cursor = conn.cursor()
    try:
        # Ler o arquivo SQL
        with open('../sql_scripts/criar_tabela_demonstracao_contabil.sql', 'r') as file:
            query_criar_tabela_contabil = file.read()
        # Substituir o placeholder pelo nome real da tabela
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

# Exemplo de uso:
def main():
    df_unico = ler_e_concatenar_csv(diretorio_destino)
    if df_unico is not None:
        print("CSV concatenado com sucesso!")
        df_unico = df_unico.tail(400000)
    else:
        print("Não foi possível concatenar os CSVs.")

    conn = conectar_banco()
    criar_tabela_unica(conn, "demonstracao_contabil")
    importar_dados(conn, "demonstracao_contabil", df_unico)


main()






