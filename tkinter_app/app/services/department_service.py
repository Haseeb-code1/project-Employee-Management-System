from app.utils.db import fetch_all, execute_query

def get_all_departments():
    query = "SELECT * FROM departments"
    return fetch_all(query)

def add_department(name):
    query = "INSERT INTO departments (name) VALUES (%s)"
    return execute_query(query, (name,))

def update_department(dept_id, name):
    query = "UPDATE departments SET name=%s WHERE id=%s"
    return execute_query(query, (name, dept_id))

def delete_department(dept_id):
    query = "DELETE FROM departments WHERE id=%s"
    return execute_query(query, (dept_id,))
