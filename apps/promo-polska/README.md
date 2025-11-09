# PromoPolska

Local deals and coupons aggregator for Polish retailers

## Features

- Web Scraping
- Deals Aggregation
- User Favorites

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

Visit http://localhost:3003

## License

MIT
