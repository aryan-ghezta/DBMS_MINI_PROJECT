/* ------------------------------------------------------
   FUNCTION: loyalty_points
   Calculates loyalty points based on total amount spent.
   Formula: 1 point per ₹100 spent
------------------------------------------------------ */
CREATE FUNCTION loyalty_points(total_amount DECIMAL(10,2))
RETURNS INT
DETERMINISTIC
RETURN FLOOR(total_amount / 100);



/* ------------------------------------------------------
   PROCEDURE: get_customer_spending
   Input: Customer ID
   Output: Customer name + total spending across all orders
------------------------------------------------------ */
DELIMITER $$

CREATE PROCEDURE get_customer_spending(IN p_customer_id INT)
BEGIN
    SELECT 
        c.fname, 
        c.lname, 
        SUM(o.total_amount) AS total_spent
    FROM customer c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.customer_id = p_customer_id
    GROUP BY c.customer_id;
END$$

DELIMITER ;



/* ------------------------------------------------------
   TRIGGER: set_payment_date
   Purpose:
   - Automatically sets today's date if Payment_date is NULL
   - Trigger runs BEFORE INSERT on payment table
------------------------------------------------------ */
DELIMITER $$

CREATE TRIGGER set_payment_date
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    IF NEW.Payment_date IS NULL THEN
        SET NEW.Payment_date = CURDATE();
    END IF;
END$$

DELIMITER ;