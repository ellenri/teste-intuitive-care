import os

from banco_dados.operadoras_ativas.operadoras_ativas import baixar_relatorio_operadoras_ativas
from constants import output_diretorio

url_operadoras_ativas_ans = 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/'
diretorio_anexos = output_diretorio()
diretorio_operadoras_ativas = os.path.join("..",diretorio_anexos,"operadoras_ativas_ans")

os.makedirs(diretorio_operadoras_ativas, exist_ok=True)

baixar_relatorio_operadoras_ativas(url_operadoras_ativas_ans, diretorio_operadoras_ativas)