-- 01_ch01_workflow: SQL examples (SQLite, data/banksia.db)

SELECT '[' || state || ']' AS state_value,
       COUNT(*) AS n
FROM mallee_customers
GROUP BY state
ORDER BY n DESC;

