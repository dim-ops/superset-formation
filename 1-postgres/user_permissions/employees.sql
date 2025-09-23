CREATE TABLE employees (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    region VARCHAR(20)
);

INSERT INTO employees VALUES
(1, 'Alice', 'Johnson', 'Finance', 75000, '2020-01-15', 'North'),
(2, 'Bob', 'Smith', 'IT', 85000, '2019-06-20', 'South'),
(3, 'Carol', 'Brown', 'Finance', 68000, '2021-03-10', 'North'),
(4, 'David', 'Wilson', 'HR', 62000, '2020-11-05', 'South'),
(5, 'Eve', 'Davis', 'IT', 92000, '2018-09-12', 'North'),
(6, 'Frank', 'Miller', 'Sales', 58000, '2022-01-08', 'South');
