USE testdatabase;

-- employees 테이블 생성
CREATE TABLE employees(
	id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100),
    salary DECIMAL(10, 2)
);

SELECT * FROM employees;

-- employees 테이블에 데이터 생성
INSERT INTO employees(name, position, salary)
VALUES ('혜린', 'PM', 90000),
	   ('은우', 'Frontend', 80000),
       ('가을', 'Backend', 92000),
       ('지수', 'Frontend', 7800),
       ('민혁', 'Frontend', 96000),
       ('하온', 'Backend', 1300000);

-- 모든 직원의 이름과 연봉만 조회
SELECT name, salary FROM employees;

-- 1.Frontend중에서 연봉이 90000 이하인 직원의 이름과 연봉 조회
SELECT name, salary FROM employees
WHERE position = "Frontend" AND salary <= 90000;

-- 2.PM 모든 직원의 연봉을 10% 인상 후 조회

-- 세이프 모드 끄기
SET SQL_SAFE_UPDATES = 0;
 
UPDATE employees
SET salary = salary * 1.1
WHERE position = 'PM';
SELECT * FROM employees;

-- 3.모든 Backend 직원의 연봉을 5% 인상
UPDATE employees
SET salary = salary * 1.05
WHERE position = "Backend";

-- 4.민혁 사원의 데이터 삭제
DELETE FROM employees(name = '민혁');
-- 정답
DELETE FROM employees WHERE name = '민혁';
 
-- 5.모든 직원을 position별로 그룹화하여 각 직책의 평균 연봉 계산
SELECT * FROM employees
    avg(salary) AS avg
GROUP BY position;
-- 정답
SELECT position, AVG(salary) AS average_salary
FROM employees
GROUP BY position;

-- 6.employees 테이블 삭제
DROP TABLE employees;
