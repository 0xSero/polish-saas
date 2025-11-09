# Dokumentownik

Personal document expiry tracker for Polish documents

## Features

- Document Storage
- Expiry Alerts
- Secure Vault

## Tech Stack

### Backend
- Flask
- PostgreSQL
- Celery + Redis

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

## Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Visit http://localhost:3008

## License

MIT
