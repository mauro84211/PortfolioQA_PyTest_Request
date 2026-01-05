import pytest
import requests
import faker
from config import config
from schemas.factories import generate_fake_booking_data


@pytest.fixture
def auth_token():
    url = config.BASE_URL + config.AUTH_ENDPOINT
    payload = config.DEFAULT_CREDENTIALS 
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()["token"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Falló autenticación: {e}")

@pytest.fixture
def existing_booking_id(auth_token):   
    url = config.BASE_URL + config.BOOKING_ENDPOINT
    payload = generate_fake_booking_data()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    booking_id = response.json()["bookingid"]
    yield booking_id  
    headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={auth_token}"
        }
    response = requests.delete(f"{config.BASE_URL + config.BOOKING_ENDPOINT}/{booking_id}", headers=headers)