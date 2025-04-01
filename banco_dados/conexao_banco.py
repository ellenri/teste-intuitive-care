from dotenv import load_dotenv
import os

import psycopg2

from banco_dados.operadoras_arquivo import executar_queries_operadoras_arquivo

load_dotenv()

def conectar_banco():

    db_host = os.environ.get('POSTGRES_HOST')  # 'db' é o nome do serviço no docker-compose
    db_port = os.environ.get('POSTGRES_PORT', '5432')
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_name = os.environ.get('POSTGRES_DB')

    print(db_host)
    print(db_password)
    print(db_user)

    db_params = {
        'dbname': db_name,
        'user': db_user,
        'password': db_password,
        'host': db_host,
        'port': db_port
    }

    print(db_params)

    try:
        # Estabelecer conexão com o banco de dados
        conn = psycopg2.connect(**db_params)
        print("Conexão com o banco de dados estabelecida com sucesso.")

        # Chamar a função para executar as queries
        executar_queries_operadoras_arquivo(conn)

    except psycopg2.Error as e:
        print(f"Erro de conexão com o banco de dados: {e}")

    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

conectar_banco()