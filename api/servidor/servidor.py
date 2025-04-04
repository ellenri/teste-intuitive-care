import csv
import math
import os.path
from flask_cors import CORS


from flask import Flask, request, jsonify

from constants import output_diretorio

diretorio_anexos = output_diretorio()


CSV_FILE_PATH = os.path.join("..",diretorio_anexos,"operadoras_ativas_ans", "Relatorio_cadop.csv" )  # <<<--- COLOQUE O NOME DO SEU ARQUIVO CSV AQUI
ITEMS_PER_PAGE_DEFAULT = 20
ENCODING = 'utf-8'

print(CSV_FILE_PATH)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def load_data_from_csv(file_path):
    try:
        data = []
        with open(file_path, mode='r', encoding=ENCODING, newline='') as infile:
            reader = csv.DictReader(infile, delimiter=';')
            if not reader.fieldnames:
                return [], []
            headers = reader.fieldnames
            data = list(reader)
            print(f"Sucesso: {len(data)} linhas carregadas. Cabeçalhos: {headers}")
            print("Primeiras linhas dos dados:", data[:5])
        return data, headers
    except FileNotFoundError:
        return [], []

DATA_CACHE, HEADERS = load_data_from_csv(CSV_FILE_PATH)

@app.route('/data', methods=['GET'])
def get_paginated_data():

    if not DATA_CACHE:
        return jsonify({"error": "Dados não carregados ou arquivo CSV não encontrado/inválido."}), 500

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', ITEMS_PER_PAGE_DEFAULT))
    except ValueError:
        return jsonify({"error": "Parâmetros 'page' e 'per_page' devem ser números inteiros."}), 400

    if page < 1 or per_page < 1:
        return jsonify({"error": "Parâmetros 'page' e 'per_page' devem ser números positivos."}), 400

    total_items = len(DATA_CACHE)
    total_pages = math.ceil(total_items / per_page)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    if start_index >= total_items and total_items > 0:
        return jsonify({
            "message": f"Página {page} solicitada, mas a última página é {total_pages}.",
            "data": [],
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        }), 404

    paginated_data = DATA_CACHE[start_index:end_index]
    for row in paginated_data:
        print("Chaves do dicionário:", row.keys())
        for key, value in row.items():
            print(f"Chave: {key}, Valor: {value}, Tipo: {type(value)}")
            if value is None:
                row[key] = ""
            if type(value) is list:
                row[key] = str(value)

    return jsonify({
        "data": paginated_data,
        "headers": HEADERS,
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages
    })

@app.route('/search', methods=['GET'])
def search_data():
    if not DATA_CACHE:
        return jsonify({"error": "Dados não carregados ou arquivo CSV não encontrado/inválido."}), 500

    query = request.args.get('query', '').strip()

    if not query:
        return jsonify({"error": "Parâmetro 'query' é obrigatório para a busca."}), 400

    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', ITEMS_PER_PAGE_DEFAULT))
    except ValueError:
        return jsonify({"error": "Parâmetros 'page' e 'per_page' devem ser números inteiros."}), 400

    if page < 1 or per_page < 1:
        return jsonify({"error": "Parâmetros 'page' e 'per_page' devem ser números positivos."}), 400


    query_lower = query.lower()
    results = []


    for row in DATA_CACHE:
        match_found = False
        for value in row.values():
            if value is not None and query_lower in str(value).lower():
                match_found = True
                break
        if match_found:
            results.append(row)

    total_items = len(results)
    total_pages = math.ceil(total_items / per_page)

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    if start_index >= total_items > 0:
        return jsonify({
            "message": f"Página {page} solicitada, mas a última página é {total_pages}.",
            "data": [],
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": total_pages
        }), 404

    paginated_results = results[start_index:end_index]

    for row in paginated_results:
        for key, value in row.items():
            if value is None:
                row[key] = ""
            if type(value) is list:
                row[key] = str(value)


    return jsonify({
        "data": paginated_results,
        "headers": HEADERS,
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "query": query
    })


if __name__ == '__main__':
    if load_data_from_csv(CSV_FILE_PATH):
        print(f"Iniciando servidor Flask na porta 5000...")
        app.run(debug=True, use_reloader=False)
    else:
        print("Servidor Flask não iniciado devido a erro no carregamento do CSV.")