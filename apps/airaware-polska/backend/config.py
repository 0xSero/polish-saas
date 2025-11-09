from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/airaware"
    redis_url: str = "redis://localhost:6379/1"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Air Quality APIs
    gios_api_url: str = "https://api.gios.gov.pl/pjp-api/rest"
    openaq_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
