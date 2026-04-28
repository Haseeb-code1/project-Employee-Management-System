from app.utils.db import fetch_all, execute_query

def get_all_leaves():
    query = """
        SELECT l.id, e.name, l.start_date, l.end_date, l.status 
        FROM leaves l
        JOIN employees e ON l.employee_id = e.id
    """
    return fetch_all(query)

def apply_leave(employee_id, start_date, end_date):
    query = "INSERT INTO leaves (employee_id, start_date, end_date) VALUES (%s, %s, %s)"
    return execute_query(query, (employee_id, start_date, end_date))

def update_leave_status(leave_id, status):
    query = "UPDATE leaves SET status=%s WHERE id=%s"
    return execute_query(query, (status, leave_id))
