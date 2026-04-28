IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'ems_db')
BEGIN
    CREATE DATABASE ems_db;
END
GO

USE ems_db;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users')
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL CHECK (role IN ('Admin', 'HR', 'Employee'))
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'departments')
BEGIN
    CREATE TABLE departments (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'employees')
BEGIN
    CREATE TABLE employees (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20),
        department_id INT,
        salary DECIMAL(10,2),
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'attendance')
BEGIN
    CREATE TABLE attendance (
        id INT IDENTITY(1,1) PRIMARY KEY,
        employee_id INT,
        date DATE NOT NULL,
        status VARCHAR(20) NOT NULL CHECK (status IN ('Present', 'Absent', 'Half Day', 'Leave')),
        FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'leaves')
BEGIN
    CREATE TABLE leaves (
        id INT IDENTITY(1,1) PRIMARY KEY,
        employee_id INT,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
        FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'payroll')
BEGIN
    CREATE TABLE payroll (
        id INT IDENTITY(1,1) PRIMARY KEY,
        employee_id INT,
        salary DECIMAL(10,2) NOT NULL,
        bonus DECIMAL(10,2) DEFAULT 0,
        deductions DECIMAL(10,2) DEFAULT 0,
        month_year VARCHAR(20) NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
    );
END
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'performance')
BEGIN
    CREATE TABLE performance (
        id INT IDENTITY(1,1) PRIMARY KEY,
        employee_id INT,
        rating INT CHECK (rating BETWEEN 1 AND 5),
        feedback TEXT,
        date DATE NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
    );
END
GO

-- Insert default admin user (password: admin123)
IF NOT EXISTS (SELECT 1 FROM users WHERE username = 'admin')
BEGIN
    INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'Admin');
END
GO
