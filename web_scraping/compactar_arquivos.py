import os
import zipfile

def compactar_arquivos(arquivos_anexos, nome_arquivo_compactado):
    with zipfile.ZipFile(nome_arquivo_compactado, 'w') as zipf:
        for arquivo in arquivos_anexos:
            zipf.write(arquivo, os.path.basename(arquivo))
            print(f"Arquivos compactados em: {nome_arquivo_compactado}")


def compactar_csv(arquivo_csv, nome_arquivo_zip):
    with zipfile.ZipFile(nome_arquivo_zip, 'w') as zipf:
        zipf.write(arquivo_csv, os.path.basename(arquivo_csv))
    print(f"Arquivo CSV compactado em: {nome_arquivo_zip}")