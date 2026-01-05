
import requests
from config import config
from schemas.factories import generate_fake_booking_data

"""Creates a new auth token to use for access to the PUT and DELETE /booking"""
def test_auth_token():
    """Tests that a POST to /auth with correct credentials returns a successful response with a valid auth token."""
    url = config.BASE_URL + config.AUTH_ENDPOINT
    payload = config.DEFAULT_CREDENTIALS 
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    
"""Test expired or invalid auth token"""
def test_invalid_auth_token():
    """Tests that a PUT to /booking with an invalid auth token returns a 403 Forbidden response."""
    booking_id = 1  
    url = f"{config.BASE_URL + config.BOOKING_ENDPOINT}/{booking_id}"
    payload = generate_fake_booking_data()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": "token=invalidtoken123"
    }

    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == 403   # Forbidden due to invalid token