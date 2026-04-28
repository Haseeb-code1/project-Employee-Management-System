import pytest
from unittest.mock import patch
from app.services.department_service import get_all_departments, add_department

@patch('app.services.department_service.fetch_all')
def test_get_all_departments(mock_fetch_all):
    mock_fetch_all.return_value = [{'id': 1, 'name': 'Engineering'}]
    result = get_all_departments()
    assert len(result) == 1
    assert result[0]['name'] == 'Engineering'

@patch('app.services.department_service.execute_query')
def test_add_department(mock_execute_query):
    mock_execute_query.return_value = 1
    result = add_department('HR')
    assert result == 1
