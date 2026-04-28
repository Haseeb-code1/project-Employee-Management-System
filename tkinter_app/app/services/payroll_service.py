from app.utils.db import fetch_all, execute_query

def get_all_payroll():
    query = """
        SELECT p.id, e.name, p.salary, p.bonus, p.deductions, p.month_year 
        FROM payroll p
        JOIN employees e ON p.employee_id = e.id
    """
    return fetch_all(query)

def add_payroll(employee_id, salary, bonus, deductions, month_year):
    query = "INSERT INTO payroll (employee_id, salary, bonus, deductions, month_year) VALUES (%s, %s, %s, %s, %s)"
    return execute_query(query, (employee_id, salary, bonus, deductions, month_year))
