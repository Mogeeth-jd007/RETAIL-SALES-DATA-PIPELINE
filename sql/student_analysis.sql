-- 1. Total students
SELECT COUNT(*) AS total_students
FROM students;

-- 2. Average marks
SELECT ROUND(AVG(marks), 2) AS average_marks
FROM students;

-- 3. Student count by course
SELECT
    course,
    COUNT(*) AS student_count
FROM students
GROUP BY course
ORDER BY student_count DESC;

-- 4. Top 5 students by marks
SELECT
    student_name,
    course,
    marks
FROM students
ORDER BY marks DESC
LIMIT 5;