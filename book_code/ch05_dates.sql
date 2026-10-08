-- 05_ch05_dates: SQL examples (SQLite, data/banksia.db)

SELECT date('1899-12-30', '+41275 days') AS norwood,
       date('1899-12-30', '+45474 days') AS regional;


SELECT CAST(strftime('%Y', order_ts_utc) AS INTEGER)
       + (CAST(strftime('%m', order_ts_utc) AS INTEGER)
          >= 7) AS fin_year,
       COUNT(*) AS orders
FROM web_orders
GROUP BY fin_year;

