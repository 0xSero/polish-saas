# Imieniny Reminder

A calendar app that reminds users of friends' name days (Polish tradition).

## Features

- 📅 Complete Polish name day database
- 👥 Manage contacts with their name days
- 🔔 Automated reminders (email and push notifications)
- 📊 Calendar view with upcoming name days
- ⚙️ Customizable notification preferences

## Tech Stack

### Backend
- Django 5.0
- Django REST Framework
- PostgreSQL
- Celery + Redis for background tasks
- Docker support

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Heroicons

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
python manage.py migrate

# Load Polish name days data
python manage.py shell
>>> from core.tasks import load_polish_name_days
>>> load_polish_name_days.delay()

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver 8001

# In another terminal, start Celery worker
celery -A imieniny worker -l info

# In another terminal, start Celery beat
celery -A imieniny beat -l info
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

Visit http://localhost:3001

## API Endpoints

- `GET /api/namedays/` - List all name days
- `GET /api/namedays/today/` - Today's name days
- `GET /api/namedays/upcoming/` - Upcoming name days (next 7 days)
- `GET /api/namedays/search/?q=<name>` - Search name days
- `GET /api/contacts/` - List user contacts
- `POST /api/contacts/` - Create new contact
- `GET /api/contacts/upcoming_namedays/` - Contacts with upcoming name days
- `GET /api/preferences/` - Get notification preferences
- `PUT /api/preferences/` - Update notification preferences

## Monetization

One-time purchase model for full app access.

## License

MIT
