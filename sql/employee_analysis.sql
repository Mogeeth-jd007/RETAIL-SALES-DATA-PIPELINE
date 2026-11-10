-- 1. Total number of employees

SELECT
    COUNT(*) AS total_employees
FROM employees;

-- 2. Average employee salary

SELECT
    ROUND(AVG(salary), 2) AS average_salary
FROM employees;

-- 3. Employee count by department

SELECT
    department,
    COUNT(*) AS employee_count
FROM employees
GROUP BY department
ORDER BY employee_count DESC;

-- 4. Top 5 highest-paid employees

SELECT
    employee_name,
    department,
    salary
FROM employees
ORDER BY salary DESC
LIMIT 5;