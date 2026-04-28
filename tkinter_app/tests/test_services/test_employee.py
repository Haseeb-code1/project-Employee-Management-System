import unittest
from unittest.mock import patch
from app.services.employee_service import get_all_employees, add_employee

class TestEmployeeService(unittest.TestCase):
    @patch('app.services.employee_service.fetch_all')
    def test_get_all_employees(self, mock_fetch_all):
        mock_fetch_all.return_value = [{"id": 1, "name": "John Doe", "email": "john@test.com"}]
        employees = get_all_employees()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0]['name'], "John Doe")

    @patch('app.services.employee_service.execute_query')
    def test_add_employee(self, mock_execute_query):
        mock_execute_query.return_value = 1  # Last insert ID
        emp_id = add_employee("Jane Doe", "jane@test.com", "1234567890", 1, 50000)
        self.assertEqual(emp_id, 1)

if __name__ == '__main__':
    unittest.main()
