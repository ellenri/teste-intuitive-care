import os

from banco_dados.demonstracoes_contabeis.demonstracoes_contabeis import criar_tabela_unica, importar_dados, \
    ler_e_concatenar_csv, \
    diretorio_destino, diretorio_origem, extrair_arquivos_zip, baixar_demonstracoes_contabeis
from banco_dados.conexao import conectar_banco
from constants import output_diretorio, diretorio_anexo


def main():
    url_demonstracoes_contabeis = 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'
    diretorio_demonstracoes_contabeis = os.path.join("..", diretorio_anexo("demonstracoes_contabeis"))

    os.makedirs(diretorio_demonstracoes_contabeis, exist_ok=True)

    baixar_demonstracoes_contabeis(url_demonstracoes_contabeis, diretorio_demonstracoes_contabeis)

    extrair_arquivos_zip(diretorio_origem, diretorio_destino)

    df_unico = ler_e_concatenar_csv(diretorio_destino)

    conn = conectar_banco()

    criar_tabela_unica(conn, "demonstracao_contabil")

    importar_dados(conn, "demonstracao_contabil", df_unico)

main()