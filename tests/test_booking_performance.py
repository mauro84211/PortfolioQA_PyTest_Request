
import requests
import time
from config import config
from schemas.factories import generate_fake_booking_data

class TestBookingPerformance:
    """Pruebas de rendimiento y SLA"""
    
    # Definir umbrales de performance (en segundos)
    SLA_POST = 1.5  # Creación debe ser < 1.5s
    SLA_GET = 0.5   # Lectura debe ser < 0.5s
    SLA_PUT = 1.5   # Actualización debe ser < 1.5s
    SLA_DELETE = 1.0  # Eliminación debe ser < 1s
    
    def test_create_booking_response_time(self):
        """Valida SLA de creación de booking"""
        payload = generate_fake_booking_data()
        
        start_time = time.perf_counter()
        response = requests.post(
            f"{config.BASE_URL}{config.BOOKING_ENDPOINT}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        end_time = time.perf_counter()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        
        # Assertion de performance
        assert response_time < self.SLA_POST, f"SLA excedido: {response_time:.2f}s > {self.SLA_POST}s"

    
    def test_get_booking_response_time(self, existing_booking_id):
        """Valida SLA de obtención de booking"""
        start_time = time.perf_counter()
        response = requests.get(
            f"{config.BASE_URL}{config.BOOKING_ENDPOINT}/{existing_booking_id}",
            headers={"Accept": "application/json"},
            timeout=10
        )
        end_time = time.perf_counter()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        
        assert response_time < self.SLA_GET, f"SLA excedido: {response_time:.2f}s > {self.SLA_GET}s"
    
    def test_update_booking_response_time(self, auth_token, existing_booking_id):
        """Valida SLA de actualización"""
        payload = generate_fake_booking_data()
        
        start_time = time.perf_counter()
        response = requests.put(
            f"{config.BASE_URL}{config.BOOKING_ENDPOINT}/{existing_booking_id}",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Cookie": f"token={auth_token}"
            },
            timeout=10
        )
        end_time = time.perf_counter()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        
        assert response_time < self.SLA_PUT, f"SLA excedido: {response_time:.2f}s > {self.SLA_PUT}s"
    
    def test_delete_booking_response_time(self, auth_token, existing_booking_id):
        """Valida SLA de eliminación"""
        start_time = time.perf_counter()
        response = requests.delete(
            f"{config.BASE_URL}{config.BOOKING_ENDPOINT}/{existing_booking_id}",
            headers={"Cookie": f"token={auth_token}"},
            timeout=10
        )
        end_time = time.perf_counter()
        
        assert response.status_code == 201
        response_time = end_time - start_time
        
        assert response_time < self.SLA_DELETE, f"SLA excedido: {response_time:.2f}s > {self.SLA_DELETE}s"
    
    def test_create_multiple_bookings_sequential_performance(self, auth_token):
        """Performance de creación secuencial (detecta degradación gradual)"""
        response_times = []
        
        for i in range(10):
            payload = generate_fake_booking_data()
            
            start_time = time.perf_counter()
            response = requests.post(
                f"{config.BASE_URL}{config.BOOKING_ENDPOINT}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            end_time = time.perf_counter()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
            
            # Cleanup inmediato
            booking_id = response.json()["bookingid"]
            requests.delete(
                f"{config.BASE_URL}{config.BOOKING_ENDPOINT}/{booking_id}",
                headers={"Cookie": f"token={auth_token}"},
                timeout=5
            )
        
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        
        # El promedio debe cumplir SLA y la desviación no debe ser extrema
        assert avg_time < self.SLA_POST, f"Promedio SLA excedido: {avg_time:.2f}s"
        assert max_time < self.SLA_POST * 2, f"Performance inconsistente: {max_time:.2f}s"
        
        print(f"\nPerformance - Secuencial: avg={avg_time:.3f}s, max={max_time:.3f}s")
    
    def test_payload_size_impact_on_performance(self):
        """Valida impacto de tamaño de payload"""
        # Payload pequeño
        small_payload = {
            "firstname": "Al",
            "lastname": "Bo",
            "totalprice": 100,
            "depositpaid": False,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-01-02"},
            "additionalneeds": "x"
        }
        
        # Payload grande
        large_payload = {
            "firstname": "A" * 50,
            "lastname": "B" * 50,
            "totalprice": 999999,
            "depositpaid": True,
            "bookingdates": {"checkin": "2024-01-01", "checkout": "2024-12-31"},
            "additionalneeds": "X" * 500  # Necesidad larga
        }
        
        for name, payload in [("small", small_payload), ("large", large_payload)]:
            start_time = time.perf_counter()
            response = requests.post(
                f"{config.BASE_URL}{config.BOOKING_ENDPOINT}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            end_time = time.perf_counter()
            
            assert response.status_code == 200
            print(f"\nPayload {name}: {end_time - start_time:.3f}s")