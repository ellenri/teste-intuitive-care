CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(255) PRIMARY KEY,
    cnpj VARCHAR(255),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(10),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(10),
    cep VARCHAR(14),
    ddd VARCHAR(10),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(255),
    regiao_de_comercializacao VARCHAR(2),
    data_registro_ans DATE
);