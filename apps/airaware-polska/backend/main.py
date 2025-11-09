from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api import auth, air_quality, alerts, subscriptions
from database import engine
from models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown


app = FastAPI(
    title="AirAware Polska API",
    description="Real-time air quality alerts for Polish cities",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(air_quality.router, prefix="/api/air-quality", tags=["Air Quality"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(subscriptions.router, prefix="/api/subscriptions", tags=["Subscriptions"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to AirAware Polska API",
        "docs": "/docs",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
