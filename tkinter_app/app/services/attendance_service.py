from app.utils.db import fetch_all, execute_query

def get_attendance():
    query = """
        SELECT a.id, e.name, a.date, a.status 
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
    """
    return fetch_all(query)

def add_attendance(employee_id, date, status):
    query = "INSERT INTO attendance (employee_id, date, status) VALUES (%s, %s, %s)"
    return execute_query(query, (employee_id, date, status))
