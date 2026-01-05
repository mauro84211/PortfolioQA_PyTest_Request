
import requests
from config import config
from schemas.booking_schemas import validate_response
from schemas.factories import generate_fake_booking_data

"""Updates a current booking"""
def test_update_booking(auth_token, existing_booking_id):
    """Tests that a PUT to /booking with correct credentials and a valid booking ID returns a successful response with the updated booking data."""
    booking_id = existing_booking_id    
    url = f"{config.BASE_URL + config.BOOKING_ENDPOINT}/{booking_id}"
    payload = generate_fake_booking_data()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    }

    response = requests.put(url, json=payload, headers=headers)

    assert response.status_code == 200
    
    booking_data = response.json()
    validated_booking = validate_response(booking_data)
    
    assert validated_booking.firstname == payload["firstname"]
    assert validated_booking.lastname == payload["lastname"]
    assert validated_booking.totalprice == payload["totalprice"]
    assert validated_booking.bookingdates.checkin == payload["bookingdates"]["checkin"]
    assert validated_booking.bookingdates.checkout == payload["bookingdates"]["checkout"]
    assert validated_booking.additionalneeds == payload["additionalneeds"]
    assert validated_booking.depositpaid == payload["depositpaid"]
    
    assert validated_booking.bookingdates.checkin < validated_booking.bookingdates.checkout 
    assert isinstance(validated_booking.totalprice, int)
    assert isinstance(validated_booking.depositpaid, bool)
    
       

"""Creates a new booking in the API"""
def test_create_booking():
    """Tests that a POST to /booking with valid booking data returns a successful response with the created booking data."""
    fake_booking_data = generate_fake_booking_data()
    
    url = config.BASE_URL + config.BOOKING_ENDPOINT
    payload = generate_fake_booking_data()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    assert response.status_code == 200
    booking_data = response.json()
    validated_booking = validate_response(booking_data)
    assert validated_booking.booking.firstname == payload["firstname"]
    assert validated_booking.booking.lastname == payload["lastname"]
    assert validated_booking.booking.totalprice == payload["totalprice"]
    assert validated_booking.booking.bookingdates.checkin == payload["bookingdates"]["checkin"]
    assert validated_booking.booking.bookingdates.checkout == payload["bookingdates"]["checkout"]
    assert validated_booking.booking.additionalneeds == payload["additionalneeds"]

    # Validación adicional de lógica de negocio
    assert validated_booking.booking.bookingdates.checkin < validated_booking.booking.bookingdates.checkout 
    # Assertion de tipo de datos
    assert isinstance(validated_booking.booking.totalprice, int)
    assert isinstance(validated_booking.booking.depositpaid, bool)
    
      

    """Deletes a booking from the API. Requires an authorization token to be set in the header"""
def test_delete_booking(auth_token, existing_booking_id):
        """Tests that a DELETE to /booking with correct credentials and a valid booking ID returns a successful response indicating the booking was deleted."""
        booking_id = existing_booking_id
        url = f"{config.BASE_URL + config.BOOKING_ENDPOINT}/{booking_id}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={auth_token}"
        }

        response = requests.delete(url, headers=headers)
        assert response.status_code == 201
        
def test_update_booking_with_invalid_token_returns_403(existing_booking_id):
    """Valida que token inválido es rechazado"""
    url = f"{config.BASE_URL + config.BOOKING_ENDPOINT}/{existing_booking_id}"
    headers = {"Cookie": "token=invalid_token"}
    
    response = requests.put(url, json={}, headers=headers)
    
    assert response.status_code == 403
    assert "Forbidden" in response.text