import re
import pdfplumber


def obter_legenda(caminho_anexo1):
    with pdfplumber.open(caminho_anexo1) as pdf:
        primeira_pagina = pdf.pages[2]
        texto = primeira_pagina.extract_text()

        resultado = {}
        if texto:
            chaves = re.findall(r'[A-Z]{2,3}:', texto)
            if chaves:
                partes = re.split(r'[A-Z]{2,3}:', texto)
                for i in range(len(chaves)):
                    chave = chaves[i][:-1]
                    valor = partes[i + 1].strip()
                    resultado[chave] = valor
        return resultado

def substituir_abreviacoes(df, legenda):
    for coluna in ['OD', 'AMB']:
        if coluna in df.columns and coluna in legenda:
            df[coluna] = df[coluna].astype(str).str.upper().replace(coluna.upper(), legenda[coluna].upper())
    return df