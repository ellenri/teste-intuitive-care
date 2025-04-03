import os

def output_diretorio():
    diretorio_anexos = os.path.join("..", "output")
    return diretorio_anexos

def diretorio_anexo(diretorio):
    return os.path.join(output_diretorio(), diretorio)
