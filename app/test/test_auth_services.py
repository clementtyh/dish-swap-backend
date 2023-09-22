import sys
import os

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

import pytest
import datetime
import jwt
from fastapi import Request, HTTPException
from services.auth_services import create_token, verify_token, validate_token
from models.response import ErrorOut

# Mock keys and algorithm for testing (replace with your actual keys and algorithm)
PRIVATE_KEY = "your_private_key"
PUBLIC_KEY = "your_public_key"
ALGORITHM = "your_algorithm"

# Mock user data for testing
user_data = {"id": 123, "username": "test_user"}

# Test cases for create_token function
def test_create_token():
    token = create_token(user_data, minutes_to_expire=30)
    assert isinstance(token, str)
    # You can also add more assertions here to check the token's content and format if needed.

# Test cases for verify_token function
def test_verify_valid_token():
    token = create_token(user_data, minutes_to_expire=30)
    payload = verify_token(token)
    assert isinstance(payload, dict)
    assert payload['id'] == user_data['id']

def test_verify_expired_token():
    expired_token = create_token(user_data, minutes_to_expire=-1)  # Expired token
    with pytest.raises(HTTPException, match="Token has expired"):
        verify_token(expired_token)

def test_verify_invalid_token():
    invalid_token = "invalid_token"  # Invalid token format
    with pytest.raises(HTTPException, match="Invalid token"):
        verify_token(invalid_token)

# Test cases for validate_token function
def test_validate_token_valid():
    valid_token = create_token(user_data, minutes_to_expire=30)
    request = Request(headers={"Authorization": f"Bearer {valid_token}"})
    user_id = validate_token(request)
    assert user_id == user_data['id']

def test_validate_token_missing_authorization_header():
    request = Request(headers={})
    with pytest.raises(HTTPException, match="Invalid authorization header"):
        validate_token(request)

def test_validate_token_invalid_authorization_header():
    request = Request(headers={"Authorization": "InvalidHeaderFormat"})
    with pytest.raises(HTTPException, match="Invalid authorization header"):
        validate_token(request)

def test_validate_token_expired_token():
    expired_token = create_token(user_data, minutes_to_expire=-1)  # Expired token
    request = Request(headers={"Authorization": f"Bearer {expired_token}"})
    with pytest.raises(HTTPException, match="Token has expired"):
        validate_token(request)

def test_validate_token_invalid_token():
    invalid_token = "invalid_token"  # Invalid token format
    request = Request(headers={"Authorization": f"Bearer {invalid_token}"})
    with pytest.raises(HTTPException, match="Invalid token"):
        validate_token(request)

# Additional test cases for create_token
def test_create_token_with_empty_data():
    token = create_token({}, minutes_to_expire=30)
    assert isinstance(token, str)

# Additional test cases for verify_token
def test_verify_token_valid_with_custom_algorithm():
    token = jwt.encode({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30), **user_data}, PRIVATE_KEY, algorithm="HS256")
    payload = verify_token(token)
    assert isinstance(payload, dict)
    assert payload['id'] == user_data['id']

# Additional test cases for validate_token
def test_validate_token_valid_with_custom_algorithm():
    valid_token = jwt.encode({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30), **user_data}, PRIVATE_KEY, algorithm="HS256")
    request = Request(headers={"Authorization": f"Bearer {valid_token}"})
    user_id = validate_token(request)
    assert user_id == user_data['id']

def test_validate_token_invalid_with_custom_algorithm():
    invalid_token = jwt.encode({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30), **user_data}, PRIVATE_KEY, algorithm="HS256")
    request = Request(headers={"Authorization": f"Bearer {invalid_token}"})
    with pytest.raises(HTTPException, match="Invalid token"):
        validate_token(request)
