from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# --- MySQL Connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pet_store"
)

# --- Dashboard Route ---
@app.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM customer;")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders;")
    total_orders = cursor.fetchone()[0]
    cursor.close()

    return render_template(
        'dashboard.html',
        total_customers=total_customers,
        total_orders=total_orders,
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

# ✅ Log Customer Route
@app.route('/log_customer', methods=['GET', 'POST'])
def log_customer():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        address = request.form['address']
        email = request.form['email']

        cursor = db.cursor()
        query = "INSERT INTO customer (fname, lname, address, email) VALUES (%s, %s, %s, %s)"
        values = (fname, lname, address, email)

        try:
            cursor.execute(query, values)
            db.commit()
            msg = "✅ Customer logged successfully!"
        except Exception as e:
            db.rollback()
            msg = f"❌ Error: {e}"
        finally:
            cursor.close()

        return render_template('log_customer.html', message=msg)
    return render_template('log_customer.html', message=None)

# ✅ Log Order Route
@app.route('/log_order', methods=['GET', 'POST'])
def log_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        order_date = request.form['order_date']
        total_amount = request.form['total_amount']
        customer_id = request.form['customer_id']
        emp_id = request.form['emp_id']

        cursor = db.cursor()
        query = """
        INSERT INTO orders (order_id, order_date, total_amount, customer_id, emp_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (order_id, order_date, total_amount, customer_id, emp_id)

        try:
            cursor.execute(query, values)
            db.commit()
            msg = "✅ Order logged successfully!"
        except Exception as e:
            db.rollback()
            msg = f"❌ Error: {e}"
        finally:
            cursor.close()
        return render_template('log_order.html', message=msg)
    return render_template('log_order.html', message=None)

# ✅ Log Payment Route
@app.route('/log_payment', methods=['GET', 'POST'])
def log_payment():
    if request.method == 'POST':
        payment_id = request.form['payment_id']
        payment_date = request.form['payment_date']
        amount = request.form['amount']
        payment_mode = request.form['payment_mode']
        order_id = request.form['order_id']

        cursor = db.cursor()
        query = """
        INSERT INTO payment (payment_id, payment_date, amount, payment_mode, order_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (payment_id, payment_date, amount, payment_mode, order_id)

        try:
            cursor.execute(query, values)
            db.commit()
            msg = "✅ Payment logged successfully!"
        except Exception as e:
            db.rollback()
            msg = f"❌ Error: {e}"
        finally:
            cursor.close()
        return render_template('log_payment.html', message=msg)
    return render_template('log_payment.html', message=None)

# ✅ Log Employee Route
@app.route('/log_employee', methods=['GET', 'POST'])
def log_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        address = request.form['address']
        salary = request.form['salary']

        cursor = db.cursor()
        query = """
        INSERT INTO employee (employee_id, name, address, salary)
        VALUES (%s, %s, %s, %s)
        """
        values = (employee_id, name, address, salary)

        try:
            cursor.execute(query, values)
            db.commit()
            msg = "✅ Employee logged successfully!"
        except Exception as e:
            db.rollback()
            msg = f"❌ Error: {e}"
        finally:
            cursor.close()
        return render_template('log_employee.html', message=msg)
    return render_template('log_employee.html', message=None)

# ✅ Log Service Route
@app.route('/log_service', methods=['GET', 'POST'])
def log_service():
    if request.method == 'POST':
        service_id = request.form['service_id']
        service_name = request.form['service_name']
        service_type = request.form['service_type']
        price = request.form['price']
        employee_id = request.form['employee_id']

        cursor = db.cursor()
        query = """
        INSERT INTO service (service_id, service_name, service_type, price, employee_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (service_id, service_name, service_type, price, employee_id)

        try:
            cursor.execute(query, values)
            db.commit()
            msg = "✅ Service logged successfully!"
        except Exception as e:
            db.rollback()
            msg = f"❌ Error: {e}"
        finally:
            cursor.close()
        return render_template('log_service.html', message=msg)
    return render_template('log_service.html', message=None)

# ✅ NEW: View Tables Route
@app.route('/view_tables', methods=['GET', 'POST'])
def view_tables():
    tables = [
        "customer", "customer_service", "employee", "Order_Details", "order_product",
        "orders", "payment", "product", "service", "supplier"
    ]
    data = []
    columns = []
    selected_table = None

    if request.method == 'POST':
        selected_table = request.form['table_name']
        cursor = db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {selected_table}")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
        except Exception as e:
            data = []
            columns = []
            selected_table = f"❌ Error: {e}"
        finally:
            cursor.close()

    return render_template('view_tables.html', tables=tables, data=data, columns=columns, selected_table=selected_table)

# ✅ Execute Query Route
@app.route('/execute_query', methods=['GET', 'POST'])
def execute_query():
    result_html = None
    message = None

    if request.method == 'POST':
        query = request.form['query']
        cursor = db.cursor()

        try:
            cursor.execute(query)

            # If the query returns rows (like SELECT)
            if query.strip().lower().startswith("select"):
                data = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                # Generate HTML table
                result_html = "<table border='1' cellpadding='5'><tr>"
                for col in columns:
                    result_html += f"<th>{col}</th>"
                result_html += "</tr>"
                for row in data:
                    result_html += "<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>"
                result_html += "</table>"
                message = f"✅ Query executed successfully! {len(data)} rows returned."
            else:
                # Non-SELECT query (INSERT/UPDATE/DELETE)
                db.commit()
                message = f"✅ Query executed successfully! {cursor.rowcount} row(s) affected."
        except Exception as e:
            db.rollback()
            message = f"❌ Error: {e}"
        finally:
            cursor.close()

    return render_template('execute_query.html', result_html=result_html, message=message)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)