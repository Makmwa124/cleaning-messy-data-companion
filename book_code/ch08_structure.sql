-- 08_ch08_structure: SQL examples (SQLite, data/banksia.db)

SELECT Store, '2025-07' AS month, "Jul-25" AS sales
FROM sales_wide
UNION ALL
SELECT Store, '2025-08', "Aug-25" FROM sales_wide
UNION ALL
SELECT Store, '2025-09', "Sep-25" FROM sales_wide
ORDER BY Store, month
LIMIT 4;

