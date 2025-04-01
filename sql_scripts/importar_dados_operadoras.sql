\COPY operadoras
FROM '../output/operadoras_ativas_ans/Relatorio_cadop.csv'
DELIMITER ','
CSV HEADER;