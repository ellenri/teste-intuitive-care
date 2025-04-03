import os
import zipfile

def compactar_arquivos(arquivos_anexos, nome_arquivo_compactado):
    with zipfile.ZipFile(nome_arquivo_compactado, 'w') as zipf:
        for arquivo in arquivos_anexos:
            zipf.write(arquivo, os.path.basename(arquivo))
            print(f"Arquivos compactados em: {nome_arquivo_compactado}")


