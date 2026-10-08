-- 02_ch02_reading: SQL examples (SQLite, data/banksia.db)

SELECT loyalty_points,
       CAST(REPLACE(loyalty_points, ',', '') AS INTEGER)
         AS points
FROM mallee_customers
WHERE loyalty_points IN ('2,447', 'N/A', '-1', '')
GROUP BY loyalty_points;


SELECT DISTINCT suburb, postcode,
       substr('0000' || postcode, -4) AS postcode_fixed
FROM mallee_customers
WHERE length(postcode) < 4;

