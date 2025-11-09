from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
from datetime import datetime

from database import get_db
from models import City, AirQualityData, User
from schemas import AirQualityResponse, City as CitySchema
from api.auth import get_current_user
from config import settings

router = APIRouter()


@router.get("/cities", response_model=List[CitySchema])
async def get_cities(db: Session = Depends(get_db)):
    """Get list of all monitored Polish cities"""
    cities = db.query(City).all()
    return cities


@router.get("/city/{city_id}", response_model=AirQualityResponse)
async def get_city_air_quality(
    city_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current air quality data for a specific city"""
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    # Get latest air quality data
    latest_data = (
        db.query(AirQualityData)
        .filter(AirQualityData.city_id == city_id)
        .order_by(AirQualityData.timestamp.desc())
        .first()
    )

    if not latest_data:
        # Fetch fresh data from GIOS API
        latest_data = await fetch_air_quality_from_gios(city, db)

    return {
        "city": city,
        "current_data": latest_data,
        "forecast": None  # Can be implemented later
    }


@router.get("/current", response_model=dict)
async def get_current_location_air_quality(
    lat: float,
    lon: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get air quality for current location (by coordinates)"""
    # Find nearest city
    # This is a simple implementation - in production, use PostGIS for geospatial queries
    cities = db.query(City).all()

    if not cities:
        raise HTTPException(status_code=404, detail="No cities available")

    # Find nearest city (simple distance calculation)
    nearest_city = min(
        cities,
        key=lambda c: ((c.latitude - lat) ** 2 + (c.longitude - lon) ** 2) ** 0.5
    )

    # Get air quality for nearest city
    latest_data = (
        db.query(AirQualityData)
        .filter(AirQualityData.city_id == nearest_city.id)
        .order_by(AirQualityData.timestamp.desc())
        .first()
    )

    if not latest_data:
        latest_data = await fetch_air_quality_from_gios(nearest_city, db)

    return {
        "city": nearest_city,
        "current_data": latest_data,
        "distance_km": round(
            ((nearest_city.latitude - lat) ** 2 + (nearest_city.longitude - lon) ** 2) ** 0.5 * 111,
            1
        )
    }


async def fetch_air_quality_from_gios(city: City, db: Session) -> AirQualityData:
    """
    Fetch air quality data from GIOS (Polish air quality monitoring system)
    API documentation: https://powietrze.gios.gov.pl/pjp/content/api
    """
    if not city.gios_station_id:
        # Create mock data for demonstration
        return create_mock_air_quality_data(city, db)

    try:
        async with httpx.AsyncClient() as client:
            # Get sensor data for the station
            response = await client.get(
                f"{settings.gios_api_url}/station/sensors/{city.gios_station_id}"
            )
            sensors = response.json()

            # Fetch data for each sensor
            air_quality_data = AirQualityData(city_id=city.id)

            for sensor in sensors:
                sensor_id = sensor['id']
                param_code = sensor['param']['paramCode']

                # Get sensor data
                data_response = await client.get(
                    f"{settings.gios_api_url}/data/getData/{sensor_id}"
                )
                sensor_data = data_response.json()

                if sensor_data and sensor_data.get('values'):
                    latest_value = next(
                        (v['value'] for v in sensor_data['values'] if v['value'] is not None),
                        None
                    )

                    # Map to our model
                    if param_code == 'PM2.5':
                        air_quality_data.pm25 = latest_value
                    elif param_code == 'PM10':
                        air_quality_data.pm10 = latest_value
                    elif param_code == 'O3':
                        air_quality_data.o3 = latest_value
                    elif param_code == 'NO2':
                        air_quality_data.no2 = latest_value
                    elif param_code == 'SO2':
                        air_quality_data.so2 = latest_value
                    elif param_code == 'CO':
                        air_quality_data.co = latest_value

            # Calculate AQI
            air_quality_data.aqi = calculate_aqi(air_quality_data)
            air_quality_data.aqi_category = get_aqi_category(air_quality_data.aqi)

            db.add(air_quality_data)
            db.commit()
            db.refresh(air_quality_data)

            return air_quality_data

    except Exception as e:
        print(f"Error fetching GIOS data: {e}")
        return create_mock_air_quality_data(city, db)


def create_mock_air_quality_data(city: City, db: Session) -> AirQualityData:
    """Create mock air quality data for demonstration"""
    import random

    air_quality_data = AirQualityData(
        city_id=city.id,
        pm25=random.uniform(10, 150),
        pm10=random.uniform(20, 200),
        o3=random.uniform(30, 180),
        no2=random.uniform(10, 100),
        so2=random.uniform(5, 50),
        co=random.uniform(0.5, 5.0),
    )

    air_quality_data.aqi = calculate_aqi(air_quality_data)
    air_quality_data.aqi_category = get_aqi_category(air_quality_data.aqi)

    db.add(air_quality_data)
    db.commit()
    db.refresh(air_quality_data)

    return air_quality_data


def calculate_aqi(data: AirQualityData) -> int:
    """Calculate Air Quality Index based on pollutant levels"""
    # Simplified AQI calculation
    # In production, use official AQI calculation formula
    aqi_values = []

    if data.pm25:
        aqi_values.append(data.pm25 * 4)  # Simplified conversion
    if data.pm10:
        aqi_values.append(data.pm10 * 2)

    return int(max(aqi_values)) if aqi_values else 50


def get_aqi_category(aqi: int) -> str:
    """Get AQI category based on index value"""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"
