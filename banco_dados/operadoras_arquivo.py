import itertools

import csv
from io import StringIO
import psycopg2

def add_empty_strings_to_array(data, expected_length):
    """Adiciona strings vazias a um array para atingir o comprimento esperado."""
    while len(data) < expected_length:
        data.append("")
    return data

def importar_dados_csv_para_postgres(conn, caminho_arquivo_csv, nome_tabela):
    """Importa dados de um arquivo CSV para uma tabela PostgreSQL."""

    cursor = conn.cursor()

    try:
        # Ler a query de criação da tabela do arquivo
        with open('../sql_scripts/criar_tabela_operadoras.sql', 'r') as arquivo_sql:
            query_criar_tabela = arquivo_sql.read()

        cursor.execute(query_criar_tabela)
        conn.commit()
        print("Tabela 'operadoras' criada com sucesso.")

        with open(caminho_arquivo_csv, 'r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            cabecalho = next(leitor_csv)  # Lê o cabeçalho do arquivo CSV
            colunas = cabecalho[0].replace(';', ',').lower()

            placeholders = ', '.join(['%s'] * len(colunas.split(',')))
            query_insercao = f"INSERT INTO {nome_tabela} ({colunas}) VALUES ({placeholders})"

            # Insere os dados linha por linha
            for linha in leitor_csv:
                csv_string = "".join(linha)

                reader = csv.reader(StringIO(csv_string), delimiter=';', quotechar='"')
                linha_corrigida = next(reader)
                print(len(linha), linha)
                print(linha_corrigida)
                print("length:", len(linha_corrigida))

                cursor.execute(query_insercao, linha_corrigida)

        conn.commit()
        print(f"Dados importados com sucesso para a tabela {nome_tabela}.")

    except (psycopg2.Error, FileNotFoundError) as e:
        conn.rollback()
        print(f"Erro ao importar dados: {e}")

    finally:
        cursor.close()


