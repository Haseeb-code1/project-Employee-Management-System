# 🏢 Employee Management System (EMS)

A complete, professional-grade desktop application built with Python and modern UI components. This application handles core HR workflows, employee data management, payroll, and performance tracking with a clean, role-based access system.

## ✨ Features

* **Modern Dark-Mode UI**: Built with `customtkinter` for a sleek, responsive, and visually appealing user experience.
* **Role-Based Access Control**: Differentiates between Admin, HR, and Employee roles.
* **Employee & Department Management**: Full CRUD operations for managing organizational structure.
* **Attendance & Leaves**: Track daily attendance and manage employee leave requests.
* **Payroll Processing**: Calculate and manage salary, bonuses, and deductions.
* **Performance Evaluations**: Keep logs of employee feedback and performance ratings.
* **Robust Error Handling**: User-friendly SQL error interception for seamless data entry.

## 🛠️ Technology Stack

* **Language**: Python 3
* **GUI Framework**: CustomTkinter / Tkinter
* **Database**: Microsoft SQL Server (T-SQL)
* **Database Driver**: `pyodbc`
* **Testing**: `pytest`, `unittest.mock`

## 📂 Architecture

The project strictly follows **Clean Architecture** patterns to ensure modularity and maintainability:
```text
tkinter_app/
│
├── app/
│   ├── models/        # Data structures
│   ├── services/      # Business logic & database operations
│   ├── utils/         # Helpers, DB connection context, UI styling
│   └── views/         # CustomTkinter GUI Frames (Login, Dashboard, etc.)
│
├── tests/             # Pytest unit testing suite mocking DB layer
├── database_setup.sql # T-SQL script to initialize tables and default admin
├── requirements.txt   # Python dependencies
└── run.py             # Application entry point
```

## 🚀 Setup & Installation

### 1. Database Configuration
1. Open Microsoft SQL Server Management Studio (SSMS).
2. Create a new database named `ems_db`.
3. Open the `tkinter_app/database_setup.sql` file and execute it in SSMS to create the required tables and insert the default Admin user.
4. *Note: The application connects to `DESKTOP-G6B47CF` using Windows Authentication by default. This can be changed in `app/utils/db.py`.*

### 2. Python Environment Setup
1. Clone the repository and navigate to the project directory:
   ```bash
   cd project-Employee-Management-System
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r tkinter_app/requirements.txt
   ```

## 🎮 How to Run

Ensure your virtual environment is active, then run:

```bash
python tkinter_app/run.py
```

### 🔑 Default Credentials
Use these credentials to log in for the first time:
* **Username**: `admin`
* **Password**: `admin123`

## 🧪 Running Tests

The application includes a comprehensive 14-case test suite that uses `unittest.mock` to validate business logic without touching the live database.

To run the tests:
```bash
cd tkinter_app
$env:PYTHONPATH="." 
pytest tests/
```
