import multiprocessing
import os

import zipfile
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import transformacao_dados





# def main():
#     url_ans = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
#     diretorio_anexos = "output"
#     nome_arquivo_compactado = os.path.join(diretorio_anexos,"anexos_ans.zip")
#     nome_arquivo_csv = os.path.join(diretorio_anexos, "tabela_anexo1.csv")
#
#     os.makedirs(diretorio_anexos, exist_ok=True)
#
#     arquivos_anexos = baixar_anexos(url_ans, diretorio_anexos)
#
#     anexo1_path = next(arquivo for arquivo in arquivos_anexos if "Anexo_I" in arquivo)
#
#
#     df_tabela = transformacao_dados.extrair_dados_anexo1(anexo1_path)
#     print("df_tabela", df_tabela)
#     legenda = transformacao_dados.extrair_legenda_anexo1(anexo1_path)
#     print("legenda", legenda)
#     df_tabela = transformacao_dados.substituir_abreviacoes(df_tabela, legenda)
#     print("df_tabela2", df_tabela)
#     df_tabela.to_csv(nome_arquivo_csv, index=False)
#     print(f"Tabela salva em: {nome_arquivo_csv}")
#
#     compactar_arquivos([nome_arquivo_csv], nome_arquivo_compactado)
#     compactar_arquivos(arquivos_anexos, nome_arquivo_compactado)
#
# if __name__ == "__main__":
#     main()