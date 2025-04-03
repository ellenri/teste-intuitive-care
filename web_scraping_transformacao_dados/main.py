import os

from constants import output_diretorio
from web_scraping_transformacao_dados.compactar_arquivos import compactar_arquivos
from web_scraping_transformacao_dados.dados_tabela_rol_procedimentos_eventos_saude.extrair_compactar_dados import \
    extrair_dados_anexo1, compactar_csv
from web_scraping_transformacao_dados.dados_tabela_rol_procedimentos_eventos_saude.substituir_colunas_od_amb import obter_legenda, \
    substituir_abreviacoes
from web_scraping_transformacao_dados.baixar_anexo import baixar_anexos

def main():

    url_ans = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

    diretorio_anexos = output_diretorio()
    nome_arquivo_csv = os.path.join(diretorio_anexos, "tabela_rol_procedimentos_eventos_saude.csv")
    nome_arquivo_zip_csv = os.path.join(diretorio_anexos, "Teste_Ellen_Ribeiro.zip")
    nome_arquivo_compactado = os.path.join(diretorio_anexos, "anexos_ans.zip")

    os.makedirs(diretorio_anexos, exist_ok=True)

    arquivos_anexos = baixar_anexos(url_ans, diretorio_anexos)

    anexo1_path = next(arquivo for arquivo in arquivos_anexos if "Anexo_I" in arquivo)
    df_tabela = extrair_dados_anexo1(anexo1_path)
    print("df_tabela", df_tabela)
    legenda = obter_legenda(anexo1_path)
    print("legenda", legenda)
    df_tabela = substituir_abreviacoes(df_tabela, legenda)
    print("df_tabela2", df_tabela)
    df_tabela.to_csv(nome_arquivo_csv, index=False)
    print(f"Tabela salva em: {nome_arquivo_csv}")

    compactar_arquivos(arquivos_anexos, nome_arquivo_compactado)
    compactar_csv(nome_arquivo_csv, nome_arquivo_zip_csv)

if __name__ == '__main__':
    main()




