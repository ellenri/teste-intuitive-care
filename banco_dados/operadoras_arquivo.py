import psycopg2

def executar_queries_operadoras_arquivo(conn):
    """Executa as queries de arquivos SQL para a tabela operadoras."""

    cursor = conn.cursor()

    try:
        # Ler a query de criação da tabela do arquivo
        with open('../sql_scripts/criar_tabela_operadoras.sql', 'r') as arquivo_sql:
            query_criar_tabela = arquivo_sql.read()

        cursor.execute(query_criar_tabela)
        conn.commit()
        print("Tabela 'operadoras' criada com sucesso.")

        # Ler a query de importação de dados do arquivo
        with open('../sql_scripts/importar_dados_operadoras.sql', 'r') as arquivo_sql:
            query_importar_dados = arquivo_sql.read()

        cursor.execute(query_importar_dados)
        conn.commit()
        print("Dados importados para a tabela 'operadoras' com sucesso.")

    except psycopg2.Error as e:
        print(f"Erro ao executar queries: {e}")
        conn.rollback()

    finally:
        cursor.close()