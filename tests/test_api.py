from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_1():
    response = client.get('/test1')
    assert response.status_code == 200
    assert response.json() == 'Hello!'