import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    db_host = os.environ.get('POSTGRES_HOST')
    db_port = os.environ.get('POSTGRES_PORT', '5432')
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_name = os.environ.get('POSTGRES_DB')

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
        return conn
    except psycopg2.Error as e:
        print(f"Erro de conexão com o banco de dados: {e}")

    # finally:
    #     if 'conn' in locals() and conn:
    #         conn.close()
    #         print("Conexão com o banco de dados fechada.")
