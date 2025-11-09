from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    alerts = relationship("Alert", back_populates="user")
    locations = relationship("UserLocation", back_populates="user")


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    voivodeship = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    gios_station_id = Column(Integer, nullable=True)

    air_quality_data = relationship("AirQualityData", back_populates="city")


class AirQualityData(Base):
    __tablename__ = "air_quality_data"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Pollutant levels
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    o3 = Column(Float, nullable=True)  # Ozone
    no2 = Column(Float, nullable=True)  # Nitrogen Dioxide
    so2 = Column(Float, nullable=True)  # Sulfur Dioxide
    co = Column(Float, nullable=True)  # Carbon Monoxide

    # Overall AQI
    aqi = Column(Integer, nullable=True)
    aqi_category = Column(String, nullable=True)  # Good, Moderate, Unhealthy, etc.

    # Raw data from API
    raw_data = Column(JSON, nullable=True)

    city = relationship("City", back_populates="air_quality_data")


class UserLocation(Base):
    __tablename__ = "user_locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="locations")
    city = relationship("City")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    # Alert threshold
    threshold_aqi = Column(Integer, default=150)  # Alert when AQI exceeds this

    # Notification preferences
    notify_email = Column(Boolean, default=True)
    notify_push = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="alerts")
    city = relationship("City")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    alert_id = Column(Integer, ForeignKey("alerts.id"), nullable=False)

    message = Column(String, nullable=False)
    notification_type = Column(String, nullable=False)  # email, push
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    success = Column(Boolean, default=True)
