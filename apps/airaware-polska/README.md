# AirAware Polska

Real-time air quality monitoring and alert system for Polish cities.

## Features

- 🌍 Real-time air quality data for 20+ Polish cities
- 📊 AQI (Air Quality Index) monitoring
- 🔔 Customizable alerts when pollution exceeds thresholds
- 📧 Email and push notifications
- 📱 Mobile-friendly interface
- 🗺️ Interactive map view
- 💰 Premium subscription for advanced features

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy + PostgreSQL
- Celery + Redis for background tasks
- GIOS API integration (Polish air quality monitoring)
- JWT authentication

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Leaflet for maps

## Getting Started

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Seed cities
python seed_cities.py

# Run server
uvicorn main:app --reload --port 8002

# In another terminal, start Celery worker
celery -A tasks worker -l info

# In another terminal, start Celery beat
celery -A tasks beat -l info
```

### Frontend Setup

```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env.local

# Run development server
npm run dev
```

Visit http://localhost:3002

## API Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `GET /api/air-quality/cities` - List all cities
- `GET /api/air-quality/city/{id}` - Get air quality for specific city
- `GET /api/air-quality/current` - Get air quality for current location
- `GET /api/alerts/` - List user's alerts
- `POST /api/alerts/` - Create new alert
- `PUT /api/alerts/{id}` - Update alert
- `DELETE /api/alerts/{id}` - Delete alert
- `POST /api/subscriptions/subscribe` - Subscribe to premium

## Monetization

Freemium model:
- Free: 1 alert, basic features, hourly updates
- Premium (monthly subscription): Unlimited alerts, faster updates, historical data, forecasts

## Data Sources

- GIOS (Główny Inspektorat Ochrony Środowiska) API
- OpenAQ API as fallback

## License

MIT
