import pytest
from unittest.mock import patch
from app.services.performance_service import get_all_performance, add_performance

@patch('app.services.performance_service.fetch_all')
def test_get_all_performance(mock_fetch_all):
    mock_fetch_all.return_value = [{'id': 1, 'rating': 5}]
    result = get_all_performance()
    assert result[0]['rating'] == 5

@patch('app.services.performance_service.execute_query')
def test_add_performance(mock_execute_query):
    mock_execute_query.return_value = 1
    result = add_performance(1, 5, 'Great work', '2023-10-01')
    assert result == 1
