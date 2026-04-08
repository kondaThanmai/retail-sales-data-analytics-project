CREATE DATABASE business_analytics;
USE business_analytics;
CREATE TABLE fact_orders (
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    order_purchase_timestamp DATETIME,
    order_year INT,
    order_month INT,
    order_month_name VARCHAR(20),
    order_revenue DECIMAL(10,2),
    customer_city VARCHAR(50),
    customer_state VARCHAR(10)
);
SHOW TABLES;
SELECT COUNT(*) FROM fact_orders;
SELECT order_status, COUNT(*) 
FROM fact_orders
GROUP BY order_status;






