WITH data_limite AS (
    SELECT to_date(MAX(data), 'YYYY-MM-DD') AS max_data
    FROM demonstracao_contabil
),
periodo AS (
    SELECT max_data, (max_data - INTERVAL '1 year') AS inicio
    FROM data_limite
)
SELECT
    reg_ans AS operadora,
    SUM(
        COALESCE(replace(vl_saldo_inicial, ',', '.')::numeric, 0) -
        COALESCE(replace(vl_saldo_final, ',', '.')::numeric, 0)
    ) AS total_despesas
FROM demonstracao_contabil, periodo
WHERE
    descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS NA MODALIDADE DE PAGAMENTO POR PROCEDIMENTO'
    AND to_date(data, 'YYYY-MM-DD') BETWEEN inicio AND max_data
GROUP BY reg_ans
ORDER BY total_despesas DESC
LIMIT 10;
