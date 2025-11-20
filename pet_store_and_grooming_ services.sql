CREATE TABLE customer (
  Customer_id INT AUTO_INCREMENT PRIMARY KEY,
  Fname VARCHAR(50),
  Lname VARCHAR(50),
  Address VARCHAR(100),
  Email VARCHAR(100)
);

INSERT INTO customer (Customer_id, Fname, Lname, Address, Email) VALUES
(101,'Aryan','Sharma','123 MG Road, Bangalore','aryan008@gmail.com'),
(102,'Neha','Reddy','45 Residency Road, Hyderabad','neha.reddy@example.com'),
(103,'Rahul','Verma','78 Park Street, Kolkata','rahul.verma@example.com'),
(104,'Aryan','Sharma','Bangalore','aryan008@gmail.com'),
(105,'Aryan','Thakur','Bangalore','aryan@gmail.com'),
(108,'Hemant','Shamra','Jp nagar','hemath02@example.com'),
(109,'John','Doe','123 Pet Street, Bangalore','john02@gmail.com');

CREATE TABLE employee (
  Employee_id INT PRIMARY KEY,
  Name VARCHAR(50),
  Address VARCHAR(100),
  Salary DECIMAL(10,2)
);

INSERT INTO employee VALUES
(1,'Anjali Mehta','56 JP Nagar, Bangalore',55000.00),
(2,'Karan Singh','22 Civil Lines, Delhi',62000.00),
(3,'Priya Nair','14 MG Road, Kochi',48000.00);


CREATE TABLE product (
  Product_id INT PRIMARY KEY,
  Product_name VARCHAR(100),
  Price DECIMAL(10,2),
  Category VARCHAR(50)
);

INSERT INTO product VALUES
(1,'Pedigree',1200.00,'Dog Food'),
(2,'Ball',150.00,'Toys'),
(3,'Leash',450.00,'Accessories');

CREATE TABLE supplier (
  Supplier_id INT PRIMARY KEY,
  Name VARCHAR(100),
  Email VARCHAR(100),
  Address VARCHAR(100),
  Prod_id INT,
  FOREIGN KEY (Prod_id) REFERENCES product(Product_id)
);

INSERT INTO supplier VALUES
(301,'PetMart','contact@petmart.com','12 MG Road, Bangalore',1),
(302,'ToyLand','info@toyland.com','45 Park Street, Kolkata',2),
(303,'PetAccessories','sales@petaccessories.com','78 Residency Road, Hyderabad',3);

CREATE TABLE service (
  Service_id INT PRIMARY KEY,
  Service_Name VARCHAR(100),
  Service_Type VARCHAR(50),
  Price DECIMAL(10,2),
  Employee_id INT,
  FOREIGN KEY (Employee_id) REFERENCES employee(Employee_id)
);

INSERT INTO service VALUES
(401,'Grooming','Basic',500.00,1),
(402,'Training','Advanced',1000.00,2),
(403,'Vaccination','Standard',300.00,3),
(404,'Grooming','Basic',1300.00,2);

CREATE TABLE customer_service (
  service_id INT,
  customer_id INT,
  PRIMARY KEY (service_id, customer_id),
  FOREIGN KEY (service_id) REFERENCES service(Service_id),
  FOREIGN KEY (customer_id) REFERENCES customer(Customer_id)
);

INSERT INTO customer_service VALUES
(401,101),
(402,102),
(403,103);

CREATE TABLE orders (
  Order_id INT PRIMARY KEY,
  Order_date DATE,
  Total_amount DECIMAL(10,2),
  Customer_id INT,
  Emp_id INT,
  FOREIGN KEY (Customer_id) REFERENCES customer(Customer_id),
  FOREIGN KEY (Emp_id) REFERENCES employee(Employee_id)
);

INSERT INTO orders VALUES
(1,'2025-10-02',250.00,101,1),
(2,'2025-10-02',120.50,102,2),
(3,'2025-10-03',500.00,103,1),
(4,'2025-10-23',350.00,104,1),
(5,'2025-11-06',2000.00,105,2);

CREATE TABLE order_product (
  order_id INT,
  product_id INT,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES orders(Order_id),
  FOREIGN KEY (product_id) REFERENCES product(Product_id)
);

INSERT INTO order_product VALUES
(1,1),
(1,2),
(2,2);

CREATE TABLE Order_Details (
  Order_id INT,
  Discount DECIMAL(5,2),
  Subtotal DECIMAL(10,2)
);

INSERT INTO Order_Details VALUES
(1,10.00,225.00),
(2,5.00,114.48),
(3,0.00,500.00);

CREATE TABLE payment (
  Payment_id INT PRIMARY KEY,
  Payment_date DATE,
  Amount DECIMAL(10,2),
  Payment_mode VARCHAR(50),
  Order_id INT,
  FOREIGN KEY (Order_id) REFERENCES orders(Order_id)
);

INSERT INTO payment VALUES
(201,'2025-10-02',250.00,'Credit Card',1),
(202,'2025-10-02',120.50,'UPI',2),
(203,'2025-11-06',1200.00,'Cash',3);