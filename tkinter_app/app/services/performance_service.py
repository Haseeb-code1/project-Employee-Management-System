from app.utils.db import fetch_all, execute_query

def get_all_performance():
    query = """
        SELECT p.id, e.name, p.rating, p.feedback, p.date 
        FROM performance p
        JOIN employees e ON p.employee_id = e.id
    """
    return fetch_all(query)

def add_performance(employee_id, rating, feedback, date):
    query = "INSERT INTO performance (employee_id, rating, feedback, date) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (employee_id, rating, feedback, date))
