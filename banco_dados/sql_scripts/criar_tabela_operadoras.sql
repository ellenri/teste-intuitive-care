CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans INT8,
    cnpj INT8 PRIMARY KEY,
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(255),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(32),
    cep INT8,
    ddd FLOAT4,
    telefone FLOAT4,
    fax FLOAT4,
    endereco_eletronico VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(255),
    regiao_de_comercializacao FLOAT4,
    data_registro_ans VARCHAR(255)
);