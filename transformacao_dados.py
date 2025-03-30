import re

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

# def extrair_legenda_anexo1(caminho_anexo1):
#     with pdfplumber.open(caminho_anexo1) as pdf:
#         legenda = {}
#         for pagina in pdf.pages:
#             texto = pagina.extract_text()
#             if texto:
#                 pares = re.findall(r'([A-Z]+)\s*:\s*([A-Za-z\s.]+)', texto)
#                 for abreviacao, definicao in pares:
#                     legenda[abreviacao] = definicao.strip()
#         return legenda

def extrair_legenda_anexo1(caminho_anexo1):
    with pdfplumber.open(caminho_anexo1) as pdf:
        primeira_pagina = pdf.pages[2]  # Apenas a primeira página
        texto = primeira_pagina.extract_text()

        resultado = {}
        if texto:
            # Encontra todas as ocorrências das chaves
            chaves = re.findall(r'[A-Z]{2,3}:', texto)
            if chaves:
                partes = re.split(r'[A-Z]{2,3}:', texto)
                for i in range(len(chaves)):
                    chave = chaves[i][:-1]  # Remove o ":" do final da chave
                    valor = partes[i + 1].strip()
                    resultado[chave] = valor
        return resultado

        # legenda = {}
        # print("texto", texto)
        # if texto:
        #     # Ajuste na regex para capturar corretamente as abreviações e descrições
        #     pares = re.findall(r'(\b[A-Z]{2,}\b)\s*:\s*([A-Za-zÀ-ÿ\s.]+)', texto)
        #     for abreviacao, definicao in pares:
        #         legenda[abreviacao] = definicao.strip()
        #
        # return legenda


def substituir_abreviacoes(df, legenda):
    for coluna, definicao in legenda.items():
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.upper().replace(coluna.upper(), definicao.upper())
    return  df
