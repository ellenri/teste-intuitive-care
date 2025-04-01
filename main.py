from dotenv import load_dotenv
import os

import psycopg2

import transformacao_dados
from banco_dados.operadoras_arquivo import executar_queries_operadoras_arquivo
from transformacao_dados.extrair import extrair_dados_anexo1
from transformacao_dados.substituir import substituir_abreviacoes
from web_scraping.baixar_anexo import baixar_anexos, baixar_demonstracoes_contabeis, baixar_relatorio_cadop
from web_scraping.compactar_arquivos import compactar_arquivos, compactar_csv

load_dotenv()

def main():
    # constantes
    url_ans = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    diretorio_anexos = "output"
    nome_arquivo_compactado = os.path.join(diretorio_anexos,"anexos_ans.zip")
    nome_arquivo_csv = os.path.join(diretorio_anexos, "tabela_rol_procedimentos_eventos_saude.csv")
    nome_arquivo_zip_csv = os.path.join(diretorio_anexos, "Teste_Ellen_Ribeiro.zip")
    url_base_demonstracoes = 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'
    url_operadoras_ativas_ans = 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/'
    diretorio_download_demonstracoes = os.path.join(diretorio_anexos,"demonstracoes_contabeis")
    diretorio_download_operadoras_ativas = os.path.join(diretorio_anexos,"operadoras_ativas_ans")

    os.makedirs(diretorio_anexos, exist_ok=True)
    os.makedirs(diretorio_download_demonstracoes, exist_ok=True)
    os.makedirs(diretorio_download_operadoras_ativas, exist_ok=True)

    arquivos_anexos = baixar_anexos(url_ans, diretorio_anexos)
    baixar_demonstracoes_contabeis(url_base_demonstracoes, diretorio_download_demonstracoes)
    baixar_relatorio_cadop(url_operadoras_ativas_ans, diretorio_download_operadoras_ativas)

    anexo1_path = next(arquivo for arquivo in arquivos_anexos if "Anexo_I" in arquivo)
    df_tabela = transformacao_dados.extrair.extrair_dados_anexo1(anexo1_path)
    print("df_tabela", df_tabela)
    legenda = transformacao_dados.extrair.extrair_legenda_anexo1(anexo1_path)
    print("legenda", legenda)
    df_tabela = transformacao_dados.substituir.substituir_abreviacoes(df_tabela, legenda)
    print("df_tabela2", df_tabela)
    df_tabela.to_csv(nome_arquivo_csv, index=False)
    print(f"Tabela salva em: {nome_arquivo_csv}")

    compactar_csv(nome_arquivo_csv, nome_arquivo_zip_csv)
    compactar_arquivos(arquivos_anexos, nome_arquivo_compactado)

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

if __name__ == "__main__":
    main()