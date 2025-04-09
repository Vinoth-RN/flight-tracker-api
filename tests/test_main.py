
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/flight-info?airline_code=AA&flight_number=100&departure_date=2025-04-10")
    assert response.status_code == 200
    assert "airline_code" in response.json()
