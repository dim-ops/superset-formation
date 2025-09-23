CREATE TABLE sales_data (
    id INT PRIMARY KEY,
    product VARCHAR(50),
    revenue DECIMAL(12,2),
    sales_date DATE,
    region VARCHAR(20),
    customer_type VARCHAR(20)
);

INSERT INTO sales_data VALUES
(1, 'Product A', 15000, '2024-01-15', 'North', 'Enterprise'),
(2, 'Product B', 8500, '2024-01-20', 'South', 'SMB'),
(3, 'Product A', 22000, '2024-02-10', 'North', 'Enterprise'),
(4, 'Product C', 12000, '2024-02-15', 'South', 'Enterprise'),
(5, 'Product B', 6500, '2024-03-05', 'North', 'SMB');
