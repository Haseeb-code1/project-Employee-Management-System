import os
import pyodbc

class DatabaseContext:
    def __init__(self):
        self.server = os.environ.get("DB_SERVER", "DESKTOP-G6B47CF")
        self.database = os.environ.get("DB_NAME", "ems_db")
        self.user = os.environ.get("DB_USER", "")
        self.password = os.environ.get("DB_PASSWORD", "")
        self.connection = None

    def __enter__(self):
        try:
            if self.user and self.password:
                conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password};TrustServerCertificate=yes;"
            else:
                conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;TrustServerCertificate=yes;"
            self.connection = pyodbc.connect(conn_str)
            return self.connection
        except Exception as e:
            raise Exception(f"Could not connect to the database. Is SQL Server running? Error: {str(e)}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

def parse_error(e_str):
    e_str = str(e_str)
    if "FOREIGN KEY" in e_str:
        return "You entered an ID (like Department ID or Employee ID) that does not exist. Please check the ID or create it first."
    elif "UNIQUE KEY" in e_str or "Violation of UNIQUE" in e_str:
        return "This record already exists. Ensure values like Email or Username are unique."
    elif "converting data type" in e_str or "Invalid character" in e_str or "numeric" in e_str.lower():
        return "Invalid input format. Please ensure you type numbers in number fields (like Salary or ID)."
    elif "date" in e_str.lower() or "datetime" in e_str.lower():
        return "Invalid date format. Please use YYYY-MM-DD format."
    elif "truncation" in e_str.lower():
        return "The text you typed is too long for the allowed field size."
    else:
        return "An unexpected database error occurred. Please check your inputs and try again."

def execute_query(query, params=None):
    with DatabaseContext() as connection:
        cursor = connection.cursor()
        try:
            clean_params = []
            for p in (params or ()):
                if isinstance(p, str):
                    p = p.strip()
                    clean_params.append(None if p == "" else p)
                else:
                    clean_params.append(p)
            
            query = query.replace('%s', '?')
            cursor.execute(query, clean_params)
            connection.commit()
            return cursor.rowcount
        except Exception as e:
            raise Exception(parse_error(e))

def fetch_all(query, params=None):
    with DatabaseContext() as connection:
        cursor = connection.cursor()
        try:
            query = query.replace('%s', '?')
            cursor.execute(query, params or ())
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except Exception as e:
            raise Exception(parse_error(e))

def fetch_one(query, params=None):
    with DatabaseContext() as connection:
        cursor = connection.cursor()
        try:
            query = query.replace('%s', '?')
            cursor.execute(query, params or ())
            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            return None
        except Exception as e:
            raise Exception(parse_error(e))
