from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200


def test_get_employee():
    employee = {
        "id": 1,
        "name": "Alice",
        "department": "IT",
        "email": "alice@example.com",
    }

    with patch(
        "routers.employees.employee_service.get_employee", return_value=employee
    ):
        response = client.get("/employees/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_employee_not_found():
    with patch("routers.employees.employee_service.get_employee", return_value=None):
        response = client.get("/employees/999")

    assert response.status_code == 404
