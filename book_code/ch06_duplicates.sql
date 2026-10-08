-- 06_ch06_duplicates: SQL examples (SQLite, data/banksia.db)

SELECT order_id, COUNT(*) AS copies
FROM web_orders
GROUP BY order_id, customer_id, order_ts_utc,
         product_code, qty, unit_price,
         ship_weight, weight_unit
HAVING COUNT(*) > 1
ORDER BY order_id
LIMIT 3;


WITH ranked AS (
  SELECT cust_no, suburb, postcode, last_updated,
         ROW_NUMBER() OVER (
           PARTITION BY cust_no
           ORDER BY last_updated DESC) AS rn
  FROM (SELECT DISTINCT * FROM mallee_customers)
)
SELECT cust_no, suburb, postcode, last_updated
FROM ranked
WHERE rn = 1 AND cust_no IN ('000032', '000078');


SELECT o.customer_id, COUNT(*) AS orders
FROM web_orders AS o
LEFT JOIN (SELECT DISTINCT cust_no
           FROM mallee_customers) AS c
  ON c.cust_no = o.customer_id
WHERE c.cust_no IS NULL
GROUP BY o.customer_id;

