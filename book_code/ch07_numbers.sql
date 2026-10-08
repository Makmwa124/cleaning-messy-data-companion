-- 07_ch07_numbers: SQL examples (SQLite, data/banksia.db)

SELECT weight_unit,
       ROUND(AVG(CASE WHEN weight_unit = 'g'
                      THEN ship_weight / 1000.0
                      ELSE ship_weight END), 2)
         AS avg_kg
FROM web_orders
GROUP BY weight_unit;


SELECT COUNT(*) AS orders,
       SUM(qty) AS items_raw,
       SUM(CASE WHEN qty IN (999, -1) THEN NULL
                ELSE qty END) AS items_clean
FROM (SELECT DISTINCT * FROM web_orders);

