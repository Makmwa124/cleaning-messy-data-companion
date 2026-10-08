-- 04_ch04_missing: SQL examples (SQLite, data/banksia.db)

SELECT COUNT(*) AS customers,
       COUNT(NULLIF(NULLIF(NULLIF(NULLIF(
         LOWER(TRIM(email)), ''), 'n/a'), 'none'), '-'))
         AS with_email
FROM mallee_customers;


WITH r AS (
  SELECT 1 AS row_no, 'Metro' AS region, 'Norwood' AS store
  UNION ALL SELECT 2, NULL, 'Marion'
  UNION ALL SELECT 3, NULL, 'Glenelg'
  UNION ALL SELECT 4, 'Regional', 'Renmark'
  UNION ALL SELECT 5, NULL, 'Berri'
), g AS (
  SELECT *, COUNT(region) OVER (ORDER BY row_no) AS grp
  FROM r
)
SELECT row_no, store,
       MAX(region) OVER (PARTITION BY grp) AS region
FROM g
ORDER BY row_no;

