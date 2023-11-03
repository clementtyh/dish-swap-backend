import os
import requests


api_url = os.getenv("TEST_URL")


def test_api_endpoint():
    # Make a GET request to the API endpoint
    response = requests.get(api_url)

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Parse the response content as JSON
    json_response = response.json()

    # Check if the response contains the expected status
    assert json_response.get("status") == "OK", f"Unexpected response content: {json_response}"
