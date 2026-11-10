-- 1. Total sales revenue

SELECT
    SUM(total_amount) AS total_revenue
FROM retail_sales;

-- 2. Total number of orders

SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM retail_sales;

-- 3. Revenue by product

SELECT
    product,
    SUM(total_amount) AS product_revenue
FROM retail_sales
GROUP BY product
ORDER BY product_revenue DESC;

-- 4. Revenue by category

SELECT
    category,
    SUM(total_amount) AS category_revenue
FROM retail_sales
GROUP BY category
ORDER BY category_revenue DESC;

-- 5. Monthly sales analysis

SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    SUM(total_amount) AS monthly_revenue
FROM retail_sales
GROUP BY sales_month
ORDER BY sales_month;

-- 6. Top customers by revenue

SELECT
    customer_name,
    SUM(total_amount) AS customer_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM retail_sales
GROUP BY customer_name
ORDER BY customer_revenue DESC
LIMIT 5;

-- 7. Average order value

SELECT
    AVG(order_total) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(total_amount) AS order_total
    FROM retail_sales
    GROUP BY order_id
);