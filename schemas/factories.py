# schemas/factories.py
from faker import Faker
from schemas.booking_schemas import BookingResponse

fake = Faker()

def generate_fake_booking_data(overrides=None):
    """Crea payload válido con datos aleatorios"""
    base = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(50, 500),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": fake.date_between(start_date='today', end_date='+30d').strftime('%Y-%m-%d'),
            "checkout": fake.date_between(start_date='+31d', end_date='+60d').strftime('%Y-%m-%d')
        },
        "additionalneeds": fake.word()
    }
    if overrides:
        base.update(overrides)
    return base