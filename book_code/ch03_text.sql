-- 03_ch03_text: SQL examples (SQLite, data/banksia.db)

SELECT COUNT(*) AS names_changed
FROM mallee_customers
WHERE full_name <>
      TRIM(REPLACE(full_name, char(160), ' '));


SELECT CASE
         WHEN UPPER(REPLACE(TRIM(state), '.', ''))
              IN ('SA', 'SOUTH AUSTRALIA', 'STH AUST')
           THEN 'SA'
         WHEN UPPER(REPLACE(TRIM(state), '.', ''))
              IN ('NT', 'NORTHERN TERRITORY')
           THEN 'NT'
       END AS state_clean,
       COUNT(*) AS n
FROM mallee_customers
GROUP BY state_clean;


SELECT phone,
       REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
         phone, ' ', ''), '(', ''), ')', ''),
         '+', ''), '-', '') AS digits
FROM mallee_customers
WHERE phone LIKE '(08)%' OR phone LIKE '+61%'
LIMIT 3;

