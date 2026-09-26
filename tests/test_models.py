import pytest
from datetime import datetime
from pydantic import ValidationError
from src.user_model import UserModel, Address, UserProfile
from src.config_model import AppConfig, SecuritySettings

def test_user_model_legacy_features():
    raw_json = '''{
        "id": 101,
        "username": "JohnDoe",
        "email": "john@company.org",
        "address": {
            "street": " 123 Main St ",
            "city": "Metropolis",
            "postal_code": "12345"
        },
        "profile": {
            "bio": "Software developer",
            "interests": ["coding", "automation"]
        }
    }'''

    user = UserModel.parse_from_json_str(raw_json)
    assert user.username == "johndoe"
    assert user.email == "john@company.org"
    assert user.address.street == "123 Main St"
    assert user.address.postal_code == "12345"
    assert user.profile.interests == ["coding", "automation"]

    # Test copy mutation
    promoted = user.clone_with_role("admin")
    assert promoted.role == "admin"
    assert user.role == "member"


def test_user_model_validation_failures():
    # Email domain check failure
    with pytest.raises((ValueError, ValidationError)):
        UserModel(
            id=1,
            username="validuser",
            email="hack@unauthorized-domain.com"
        )

    # Postal code regex failure
    with pytest.raises((ValueError, ValidationError)):
        Address(street="Test St", city="Test City", postal_code="INVALID_ZIP")


def test_config_model_sanitization():
    sec = SecuritySettings(secret_key="super_secret_key_12345")
    cfg = AppConfig(
        app_name="  ModernApp  ",
        environment="STAGING",
        max_workers=8,
        security=sec
    )

    assert cfg.app_name == "ModernApp"
    assert cfg.environment == "staging"
    
    sanitized = cfg.export_sanitized_config()
    assert sanitized["security"]["secret_key"] == "********"
    assert sanitized["max_workers"] == 8