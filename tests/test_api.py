import pytest
from fastapi.testclient import TestClient
from src.api_service import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_user_flow():
    payload = {
        "id": 50,
        "username": "AliceDev",
        "email": "alice@test.com",
        "role": "member",
        "address": {
            "street": "456 Tech Lane",
            "city": "Innovate",
            "postal_code": "98765"
        },
        "profile": {
            "interests": ["Python", "AI"]
        }
    }

    # Unauthorized test
    unauth_resp = client.post("/api/v1/users", json=payload)
    assert unauth_resp.status_code == 401

    # Authorized creation
    headers = {"X-API-Key": "secret-api-token"}
    response = client.post("/api/v1/users", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "alicedev"

    # Promote user
    promote_resp = client.post("/api/v1/users/50/promote")
    assert promote_resp.status_code == 200
    assert promote_resp.json()["user"]["role"] == "manager"


def test_config_validation_endpoint():
    config_payload = {
        "app_name": "  EnterpriseService  ",
        "environment": "production",
        "max_workers": 16,
        "security": {
            "secret_key": "enterprise_long_secret_key_99"
        }
    }

    response = client.post("/api/v1/config/validate", json=config_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["sanitized"]["security"]["secret_key"] == "********"