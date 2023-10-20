import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from services.auth_services import create_token, verify_token, validate_token

# Assuming your module is named 'your_module' and contains the provided code

@pytest.fixture
def valid_token():
    # Create a valid token for testing
    data = {"id": "user123", "username": "john_doe"}
    minutes_to_expire = 30
    return create_token(data, minutes_to_expire)


def test_create_token(valid_token):
    # Verify that the token is successfully created
    decoded_token = verify_token(valid_token)
    assert decoded_token["username"] == "john_doe"


def test_verify_valid_token(valid_token):
    # Verify that a valid token is successfully verified
    decoded_token = verify_token(valid_token)
    assert decoded_token["id"] == "user123"


def test_verify_expired_token():
    # Verify that an expired token raises an HTTPException
    expired_token = create_token({"id": "user123"}, -1)
    with pytest.raises(HTTPException):
        verify_token(expired_token)


def test_verify_invalid_token():
    # Verify that an invalid token raises an HTTPException
    invalid_token = "invalid_token"
    with pytest.raises(HTTPException):
        verify_token(invalid_token)


def test_validate_token(valid_token):
    # Test the validate_token function
    request_mock = type("RequestMock", (), {"headers": {"Authorization": f"Bearer {valid_token}"}})
    user_id = validate_token(request_mock)
    assert user_id == "user123"


def test_validate_token_missing_auth_header():
    # Test that missing Authorization header raises an HTTPException
    request_mock = type("RequestMock", (), {"headers": {}})
    with pytest.raises(HTTPException):
        validate_token(request_mock)


def test_validate_token_invalid_auth_header():
    # Test that an invalid Authorization header raises an HTTPException
    request_mock = type("RequestMock", (), {"headers": {"Authorization": "InvalidHeader"}})
    with pytest.raises(HTTPException):
        validate_token(request_mock)


def test_validate_token_invalid_token():
    # Test that an invalid token in the Authorization header raises an HTTPException
    request_mock = type("RequestMock", (), {"headers": {"Authorization": "Bearer invalid_token"}})
    with pytest.raises(HTTPException):
        validate_token(request_mock)

