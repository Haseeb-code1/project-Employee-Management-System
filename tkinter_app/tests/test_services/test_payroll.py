import pytest
from unittest.mock import patch
from app.services.payroll_service import get_all_payroll, add_payroll

@patch('app.services.payroll_service.fetch_all')
def test_get_all_payroll(mock_fetch_all):
    mock_fetch_all.return_value = [{'id': 1, 'salary': 5000}]
    result = get_all_payroll()
    assert result[0]['salary'] == 5000

@patch('app.services.payroll_service.execute_query')
def test_add_payroll(mock_execute_query):
    mock_execute_query.return_value = 1
    result = add_payroll(1, 5000, 500, 100, '10/2023')
    assert result == 1
