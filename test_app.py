import pytest
from flask import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_calculate_add(client):
    response = client.post('/fca/calculate', json={'num1': 1, 'num2': 2, 'operation': 'add'})
    print(response)
    assert response.status_code == 200

def test_calculate_subtract(client):
    response = client.post('/fca/calculate', json={'num1': 5, 'num2': 2, 'operation': 'subtract'})
    assert response.status_code == 200