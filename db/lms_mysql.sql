USE classicmodels;

SELECT * FROM products
WHERE productLine = 'Classic Cars';

SELECT * FROM orders
ORDER BY orderDate DESC
LIMIT 10 ;

SELECT * FROM payments
WHERE amount >= 10000;

SELECT o.orderNumber, c.customerName
FROM orders o
INNER JOIN customers c ON o.customerNumber = c.customerNumber;

SELECT p.productName, p.productLine, l.textDescription
FROM products p
INNER JOIN productlines l ON p.productLine = l.productLine;

SELECT e1.employeeNumber, e1.firstName, e1.lastName, e2.firstName AS "MANAGERFIRSTNAME", e2.lastName AS "MANAGERLASTNAME"
FROM employees e1
LEFT JOIN employees e2 ON e1.reportsTo = e2.employeeNumber;

SELECT e.firstName, e.lastName, e.officeCode, o.city
FROM employees e
INNER JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'San Francisco';

SELECT productLine, COUNT(*) AS productCount
FROM products
GROUP BY products.productLine;

SELECT c.customerNumber, c.customerName,
	   SUM(p.priceEach * p.quantityOrdered) AS "총주문금액"
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails p ON o.orderNumber = p.orderNumber
GROUP BY c.customerNumber, c.customerName;

SELECT p.productName, SUM(o.quantityOrdered) AS "총주문개수"
FROM products p
JOIN orderdetails o ON p.productCode = o.productCode
GROUP BY p.productName
ORDER BY "총주문개수" DESC
LIMIT 1;

SELECT o.city, SUM(od.priceEach * od.quantityOrdered) AS "총매출액"
FROM orderdetails od
JOIN orders ord ON ord.orderNumber = od.orderNumber
JOIN customers c ON ord.customerNumber = c.customerNumber
JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
JOIN offices o ON e.officeCode = o.officeCode
GROUP BY o.city
ORDER BY "총매출액" DESC
LIMIT 1;


SELECT orderNumber, SUM(priceEach * quantityOrdered) AS totalAmount
FROM orderdetails 
GROUP BY orderNumber
HAVING totalAmount >= 500;

SELECT customerNumber, SUM(amount) AS totalPayment
FROM payments
GROUP BY customerNumber
HAVING totalPayment > (SELECT AVG(amount) FROM payments);

SELECT customerName
FROM customers
WHERE customerNumber NOT IN (SELECT customerNumber FROM orders);

SELECT c.customerName, SUM(p.amount) AS "totalAmount"
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY c.customerName
ORDER BY totalAmount DESC
LIMIT 1;

SELECT c.customerName, SUM(priceEach * quantityOrdered) AS totalSpent
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY c.customerName
ORDER BY totalSpent DESC
LIMIT 1;


USE classicmodels;

INSERT INTO customers (customerNumber, customerName, contactLastName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit)
VALUES (497, 'Lastname', 'Firstname', '123-456-7890', '123 Street', 'Suite 1', 'City', 'State', 'PostalCode', 'Country', 1002, 50000.00);

UPDATE products
SET buyPrice = buyPrice * 1.10
WHERE productLine = 'Classic Cars'

UPDATE customers
SET email = 'ejfweio2@example.com'
WHERE customerNumber = 103;

UPDATE employees
SET officeCode = '3'
WHERE employeeNumber = 1002;