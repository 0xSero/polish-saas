"""
Seed Polish cities into the database
Run this script once to populate the cities table
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, City

# Major Polish cities with their coordinates
POLISH_CITIES = [
    {"name": "Warszawa", "voivodeship": "Mazowieckie", "latitude": 52.2297, "longitude": 21.0122, "gios_station_id": 14},
    {"name": "Kraków", "voivodeship": "Małopolskie", "latitude": 50.0647, "longitude": 19.9450, "gios_station_id": 10121},
    {"name": "Wrocław", "voivodeship": "Dolnośląskie", "latitude": 51.1079, "longitude": 17.0385, "gios_station_id": 114},
    {"name": "Poznań", "voivodeship": "Wielkopolskie", "latitude": 52.4064, "longitude": 16.9252, "gios_station_id": 612},
    {"name": "Gdańsk", "voivodeship": "Pomorskie", "latitude": 54.3520, "longitude": 18.6466, "gios_station_id": 170},
    {"name": "Szczecin", "voivodeship": "Zachodniopomorskie", "latitude": 53.4285, "longitude": 14.5528, "gios_station_id": 534},
    {"name": "Bydgoszcz", "voivodeship": "Kujawsko-Pomorskie", "latitude": 53.1235, "longitude": 18.0084, "gios_station_id": 224},
    {"name": "Lublin", "voivodeship": "Lubelskie", "latitude": 51.2465, "longitude": 22.5684, "gios_station_id": 402},
    {"name": "Białystok", "voivodeship": "Podlaskie", "latitude": 53.1325, "longitude": 23.1688, "gios_station_id": 633},
    {"name": "Katowice", "voivodeship": "Śląskie", "latitude": 50.2649, "longitude": 19.0238, "gios_station_id": 10140},
    {"name": "Gdynia", "voivodeship": "Pomorskie", "latitude": 54.5189, "longitude": 18.5305, "gios_station_id": 177},
    {"name": "Częstochowa", "voivodeship": "Śląskie", "latitude": 50.8118, "longitude": 19.1203, "gios_station_id": 514},
    {"name": "Radom", "voivodeship": "Mazowieckie", "latitude": 51.4027, "longitude": 21.1471, "gios_station_id": 52},
    {"name": "Toruń", "voivodeship": "Kujawsko-Pomorskie", "latitude": 53.0138, "longitude": 18.5984, "gios_station_id": 241},
    {"name": "Rzeszów", "voivodeship": "Podkarpackie", "latitude": 50.0412, "longitude": 21.9991, "gios_station_id": 453},
    {"name": "Kielce", "voivodeship": "Świętokrzyskie", "latitude": 50.8661, "longitude": 20.6286, "gios_station_id": 371},
    {"name": "Gliwice", "voivodeship": "Śląskie", "latitude": 50.2945, "longitude": 18.6714, "gios_station_id": 10123},
    {"name": "Zabrze", "voivodeship": "Śląskie", "latitude": 50.3249, "longitude": 18.7856, "gios_station_id": 10197},
    {"name": "Olsztyn", "voivodeship": "Warmińsko-Mazurskie", "latitude": 53.7784, "longitude": 20.4801, "gios_station_id": 302},
    {"name": "Bielsko-Biała", "voivodeship": "Śląskie", "latitude": 49.8224, "longitude": 19.0446, "gios_station_id": 10123},
]


def seed_cities():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if cities already exist
        existing_cities = db.query(City).count()
        if existing_cities > 0:
            print(f"Cities already seeded ({existing_cities} cities in database)")
            return

        # Add cities
        for city_data in POLISH_CITIES:
            city = City(**city_data)
            db.add(city)

        db.commit()
        print(f"Successfully seeded {len(POLISH_CITIES)} Polish cities")

    except Exception as e:
        print(f"Error seeding cities: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_cities()
