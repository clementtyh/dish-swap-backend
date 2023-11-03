import os
import requests


BASE_URL = os.getenv("TEST_URL")


def test_login_success():
    # Create a valid login payload
    login_data = {
        "email": "test@example.com",
        "password": "Test123!",
    }

    # Make a request to the login endpoint
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Parse the response JSON
    response_json = response.json()

    # Assert that the response has the expected structure
    assert response_json.get("status") == "success"
    assert "message" in response_json
    assert "payload" in response_json


def test_login_invalid_email():
    # Create a payload with an invalid email
    login_data = {
        "email": "ttest@example.com",
        "password": "Test123!",
    }

    # Make a request to the login endpoint
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    # Check if the response status code is 400 Bad Request
    assert response.status_code == 400

    # Parse the response JSON
    response_json = response.json()

    # Assert that the response has the expected structure
    assert response_json.get("status") == "error"
    assert response_json.get("message") == f"User with email '{login_data['email']}' not found"


def test_login_invalid_password():
    # Create a payload with an invalid password
    login_data = {
        "email": "test@example.com",
        "password": "TTest123!",
    }

    # Make a request to the login endpoint
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

    # Check if the response status code is 400 Bad Request
    assert response.status_code == 400

    # Parse the response JSON
    response_json = response.json()

    # Assert that the response has the expected structure
    assert response_json.get("status") == "error"
    assert response_json.get("message") == "Invalid password"
