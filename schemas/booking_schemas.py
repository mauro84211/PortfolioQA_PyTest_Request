from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional, Union
from datetime import datetime

# ==================== MODELOS DE DATOS ====================

class BookingDates(BaseModel):
    """Fechas de checkin y checkout (anidadas)"""
    checkin: str
    checkout: str
    
    @field_validator("checkin", "checkout", mode="before")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Valida formato YYYY-MM-DD"""
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {v}. Use YYYY-MM-DD")

class BookingData(BaseModel):
    """Objeto booking (para PUT/GET y el campo 'booking' de POST)"""
    firstname: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    totalprice: int = Field(..., ge=0, le=999999)
    depositpaid: bool 
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

    @field_validator("firstname", "lastname", mode="before")
    @classmethod
    def validate_names(cls, v: str) -> str:
        """Normaliza formato y valida longitud"""
        if len(v) < 2 or len(v) > 50:
            raise ValueError(f"Nombre inválido (2-50 caracteres): {v}")
        return v.title()

    @field_validator("totalprice", mode="before")
    @classmethod
    def validate_price(cls, v: int) -> int:
        """Valida rango de precio"""
        if v < 0 or v > 999999:
            raise ValueError(f"Precio fuera de rango permitido: {v}")
        return v

class BookingResponse(BaseModel):
    """Wrapper completo de POST /booking"""
    bookingid: int
    booking: BookingData
    
    class Config:
        """Configuración de Pydantic v2"""
        extra = "forbid"  # Rechazar campos no definidos
        validate_assignment = True
        from_attributes = True

# ==================== FUNCIONES DE VALIDACIÓN ====================

def validate_response(data: dict) -> Union[BookingResponse, BookingData]:
    """
    VALIDA CUALQUIER RESPUESTA DEL API:
    - POST → {bookingid, booking} → BookingResponse
    - PUT/GET → {...} → BookingData
    """
    try:
        # Detectar formato automáticamente
        if "bookingid" in data and "booking" in data:
            # POST response con wrapper
            return BookingResponse.model_validate(data)
        
        # PUT/GET response sin wrapper
        return BookingData.model_validate(data)
            
    except ValidationError as e:
        # e.json() muestra errores detallados en formato JSON
        raise AssertionError(f"❌ Schema inválido: {e.json(indent=2)}") from e