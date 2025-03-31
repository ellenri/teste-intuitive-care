
def substituir_abreviacoes(df, legenda):
    """Substitui apenas as abreviações OD e AMB pelas descrições completas."""
    for coluna in ['OD', 'AMB']:  # Itera apenas sobre as colunas OD e AMB
        if coluna in df.columns and coluna in legenda:
            df[coluna] = df[coluna].astype(str).str.upper().replace(coluna.upper(), legenda[coluna].upper())
    return df