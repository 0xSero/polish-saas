from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class CityBase(BaseModel):
    name: str
    voivodeship: str
    latitude: float
    longitude: float


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class AirQualityDataBase(BaseModel):
    pm25: Optional[float] = None
    pm10: Optional[float] = None
    o3: Optional[float] = None
    no2: Optional[float] = None
    so2: Optional[float] = None
    co: Optional[float] = None
    aqi: Optional[int] = None
    aqi_category: Optional[str] = None


class AirQualityData(AirQualityDataBase):
    id: int
    city_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class AirQualityResponse(BaseModel):
    city: City
    current_data: AirQualityData
    forecast: Optional[List[AirQualityData]] = None


class AlertBase(BaseModel):
    city_id: int
    threshold_aqi: int = 150
    notify_email: bool = True
    notify_push: bool = False


class AlertCreate(AlertBase):
    pass


class Alert(AlertBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
