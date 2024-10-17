SELECT customer, MEAN(sales)
FROM customer_sales
GROUP BY customer