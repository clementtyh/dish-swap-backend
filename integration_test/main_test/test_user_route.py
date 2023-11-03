import os
import requests


BASE_URL = os.getenv("TEST_URL")


def test_registration_failure_user_exists():
    user_data = {
        "email": "test@example.com",
        "display_name": "test_user",
        "password": "Test123!",
        "confirm_password": "Test123!",
    }

    # Make a request to the registration endpoint
    response = requests.post(f"{BASE_URL}/user/register", json=user_data)

    # Check if the response status code is 400
    assert response.status_code == 400

    # Parse the response JSON
    response_json = response.json()

    # Assert that the response has the expected structure
    assert response_json.get("status") == "error"
    assert response_json.get("message") == "User with the given email or display name already exists"


def test_registration_failure_passwords_do_not_match():
    # Create a payload that would trigger PasswordsDoNotMatchException
    user_data = {
        "email": "test@example.com",
        "display_name": "test_user",
        "password": "Test123!",
        "confirm_password": "Te!st123!",
    }

    # Make a request to the registration endpoint
    response = requests.post(f"{BASE_URL}/user/register", json=user_data)

    # Check if the response status code is 400
    assert response.status_code == 400

    # Parse the response JSON
    response_json = response.json()

    # Assert that the response has the expected structure
    assert response_json.get("status") == "error"
    assert response_json.get("message") == "Password and confirmation password must be the same"