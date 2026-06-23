-- 1. Total KPIs
SELECT
    COUNT(order_id)         AS total_orders,
    SUM(revenue)            AS total_revenue,
    SUM(profit)             AS total_profit,
    ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS profit_margin_pct,
    ROUND(AVG(revenue), 2)  AS avg_order_value
FROM sales;

-- 2. Monthly revenue trend
SELECT
    month,
    SUM(revenue)    AS revenue,
    SUM(profit)     AS profit,
    COUNT(order_id) AS orders
FROM sales
GROUP BY month
ORDER BY month;

-- 3. Revenue by category
SELECT
    category,
    SUM(revenue)    AS revenue,
    SUM(profit)     AS profit,
    COUNT(order_id) AS orders,
    ROUND(SUM(profit) * 100.0 / SUM(revenue), 2) AS margin_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- 4. Top 10 products by revenue
SELECT
    product,
    category,
    SUM(revenue)    AS revenue,
    SUM(quantity)   AS units_sold
FROM sales
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 10;

-- 5. Revenue by region
SELECT
    region,
    SUM(revenue)    AS revenue,
    SUM(profit)     AS profit,
    COUNT(order_id) AS orders
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 6. Sales channel breakdown
SELECT
    channel,
    COUNT(order_id)  AS orders,
    SUM(revenue)     AS revenue,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM sales), 2) AS share_pct
FROM sales
GROUP BY channel
ORDER BY revenue DESC;

-- 7. Year-over-year comparison
SELECT
    year,
    SUM(revenue) AS revenue,
    SUM(profit)  AS profit,
    COUNT(*)     AS orders
FROM sales
GROUP BY year
ORDER BY year;
