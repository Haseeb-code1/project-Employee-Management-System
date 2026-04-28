import pytest
from unittest.mock import patch
from app.services.leave_service import get_all_leaves, apply_leave

@patch('app.services.leave_service.fetch_all')
def test_get_all_leaves(mock_fetch_all):
    mock_fetch_all.return_value = [{'id': 1, 'status': 'Pending'}]
    result = get_all_leaves()
    assert result[0]['status'] == 'Pending'

@patch('app.services.leave_service.execute_query')
def test_apply_leave(mock_execute_query):
    mock_execute_query.return_value = 1
    result = apply_leave(1, '2023-10-01', '2023-10-05')
    assert result == 1
