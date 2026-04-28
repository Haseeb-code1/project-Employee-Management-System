from app.utils.db import fetch_all, execute_query

def get_all_employees():
    query = """
        SELECT e.id, e.name, e.email, e.phone, d.name as department, e.salary 
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
    """
    return fetch_all(query)

def add_employee(name, email, phone, department_id, salary):
    query = """
        INSERT INTO employees (name, email, phone, department_id, salary) 
        VALUES (%s, %s, %s, %s, %s)
    """
    return execute_query(query, (name, email, phone, department_id, salary))

def update_employee(emp_id, name, email, phone, department_id, salary):
    query = """
        UPDATE employees 
        SET name=%s, email=%s, phone=%s, department_id=%s, salary=%s 
        WHERE id=%s
    """
    return execute_query(query, (name, email, phone, department_id, salary, emp_id))

def delete_employee(emp_id):
    query = "DELETE FROM employees WHERE id=%s"
    return execute_query(query, (emp_id,))
