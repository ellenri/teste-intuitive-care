import os
import re
import zipfile

import pandas as pd
import pdfplumber


def extrair_dados_anexo1(caminho_anexo1):
    with pdfplumber.open(caminho_anexo1) as pdf:
        tabelas = []
        for pagina in pdf.pages:
            tabela = pagina.extract_table()
            if tabela:
                tabelas.extend(tabela)
    return pd.DataFrame(tabelas[1:], columns=tabelas[0])


def compactar_csv(arquivo_csv, nome_arquivo_zip):
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        zipf.write(arquivo_csv, os.path.basename(arquivo_csv))
    print(f"Arquivo CSV compactado em: {nome_arquivo_zip}")
