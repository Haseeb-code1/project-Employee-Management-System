import pytest
from unittest.mock import patch
from app.services.attendance_service import get_attendance, add_attendance

@patch('app.services.attendance_service.fetch_all')
def test_get_attendance(mock_fetch_all):
    mock_fetch_all.return_value = [{'id': 1, 'name': 'John', 'date': '2023-10-01', 'status': 'Present'}]
    result = get_attendance()
    assert result[0]['status'] == 'Present'

@patch('app.services.attendance_service.execute_query')
def test_add_attendance(mock_execute_query):
    mock_execute_query.return_value = 1
    result = add_attendance(1, '2023-10-01', 'Present')
    assert result == 1
