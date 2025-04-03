WITH data_limite AS (
    SELECT
        CASE
            WHEN data ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN to_date(data, 'DD/MM/YYYY')
            WHEN data ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN to_date(data, 'YYYY-MM-DD')
            ELSE NULL  -- Trata dados inválidos
        END AS max_data
    FROM demonstracao_contabil
    WHERE
      CASE
        WHEN data ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN to_date(data, 'DD/MM/YYYY')
        WHEN data ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN to_date(data, 'YYYY-MM-DD')
        ELSE NULL
      END IS NOT NULL
    ORDER BY max_data DESC
    LIMIT 1
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
    descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
    AND
    CASE
        WHEN data ~ '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN to_date(data, 'DD/MM/YYYY')
        WHEN data ~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN to_date(data, 'YYYY-MM-DD')
        ELSE NULL
    END BETWEEN inicio AND max_data
GROUP BY reg_ans
ORDER BY total_despesas DESC
LIMIT 10;