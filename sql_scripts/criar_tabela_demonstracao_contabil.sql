CREATE TABLE IF NOT EXISTS demonstracao_contabil (
    id SERIAL PRIMARY KEY,
    data VARCHAR(255),
    reg_ans INTEGER,
    cd_conta_contabil INTEGER,
    descricao TEXT,
    vl_saldo_inicial VARCHAR(255),
    vl_saldo_final VARCHAR(255)
);

CREATE INDEX idx_descricao ON demonstracao_contabil (descricao);