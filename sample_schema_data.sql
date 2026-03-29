-- Data for table: customers
INSERT INTO customers (id, name, email) VALUES (1, 'Nicole Ward', 'mitchellerica@example.net');
INSERT INTO customers (id, name, email) VALUES (2, 'David Carter', 'ericksonleslie@example.org');
INSERT INTO customers (id, name, email) VALUES (3, 'Carrie Taylor DVM', 'patricia70@example.org');
INSERT INTO customers (id, name, email) VALUES (4, 'David Wells', 'rodriguezdaniel@example.net');
INSERT INTO customers (id, name, email) VALUES (5, 'Randall Friedman', 'william51@example.net');
INSERT INTO customers (id, name, email) VALUES (6, 'Candace Thompson DDS', 'jessica39@example.net');
INSERT INTO customers (id, name, email) VALUES (7, 'Samantha Huff', 'krogers@example.net');
INSERT INTO customers (id, name, email) VALUES (8, 'Mark Palmer', 'virginiadowns@example.com');
INSERT INTO customers (id, name, email) VALUES (9, 'Debbie Anderson', 'georgejordan@example.org');
INSERT INTO customers (id, name, email) VALUES (10, 'Richard Stewart', 'jkelly@example.org');

-- Data for table: products
INSERT INTO products (id, name, price) VALUES (1, 'Krista Robinson', 2851.19);
INSERT INTO products (id, name, price) VALUES (2, 'Casey Sanders', 8884.49);
INSERT INTO products (id, name, price) VALUES (3, 'Alexis Patton', 3637.28);
INSERT INTO products (id, name, price) VALUES (4, 'William Decker', 9300.89);
INSERT INTO products (id, name, price) VALUES (5, 'Sean Martin', 1141.27);
INSERT INTO products (id, name, price) VALUES (6, 'Juan Barnes', 6395.58);
INSERT INTO products (id, name, price) VALUES (7, 'Perry Patrick', 3743.76);
INSERT INTO products (id, name, price) VALUES (8, 'Abigail Hayes', 7786.46);
INSERT INTO products (id, name, price) VALUES (9, 'Jacqueline Padilla', 521.3);
INSERT INTO products (id, name, price) VALUES (10, 'David Camacho', 8190.71);

-- Data for table: users
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (1, 'Jennifer', 'Golden', 'eric20@example.com', '2003-12-31T19:56:10', 5);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (2, 'Linda', 'Torres', 'mhartman@example.org', '2019-08-14T10:06:43', 2);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (3, 'Robert', 'Hogan', 'louisandrews@example.org', '2012-08-07T07:15:24', 3);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (4, 'Spencer', 'Welch', 'dbrewer@example.com', '1984-07-10T08:02:18', 5);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (5, 'Diane', 'Montoya', 'williamscindy@example.net', '1977-01-11T11:48:38', 8);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (6, 'Carlos', 'Navarro', 'yhayden@example.net', '2010-06-03T02:33:40', 10);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (7, 'Frank', 'Richards', 'slove@example.com', '1988-03-05T17:53:58', 8);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (8, 'Jason', 'Holmes', 'markscarlos@example.org', '2008-08-03T03:21:40', 9);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (9, 'Mary', 'Jackson', 'myersjackson@example.org', '2008-03-29T01:29:24', 6);
INSERT INTO users (id, first_name, last_name, email, created_at, customer_id) VALUES (10, 'James', 'Haley', 'sherri15@example.org', '1987-05-26T17:25:40', 5);

-- Data for table: orders
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (1, 10, 6, 97, 2026-01-17);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (2, 9, 10, 4, 2026-02-17);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (3, 2, 4, 49, 2026-01-22);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (4, 6, 10, 27, 2026-03-09);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (5, 8, 7, 12, 2026-02-16);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (6, 8, 7, 21, 2026-02-19);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (7, 4, 10, 61, 2026-02-18);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (8, 4, 2, 16, 2026-01-03);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (9, 1, 6, 72, 2026-03-13);
INSERT INTO orders (id, user_id, product_id, quantity, order_date) VALUES (10, 7, 10, 31, 2026-01-29);

