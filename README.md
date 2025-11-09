# Polish SaaS Monorepo

A comprehensive monorepo containing 10 low-maintenance B2C SaaS projects specifically designed for the Polish market. Each application addresses unique needs of Polish consumers with culturally relevant features and local language support.

## 🚀 Projects Overview

### 1. **Imieniny Reminder** 🎂
Polish name day calendar and reminder system
- **Tech**: Django + React + Celery
- **Monetization**: One-time purchase
- **Ports**: Backend 8001, Frontend 3001
- **Features**: Name day database, contact management, automated reminders

### 2. **AirAware Polska** 🌫️
Real-time air quality monitoring and alerts for Polish cities
- **Tech**: FastAPI + React + Celery
- **Monetization**: Freemium subscription
- **Ports**: Backend 8002, Frontend 3002
- **Features**: GIOŚ API integration, customizable alerts, 20+ Polish cities

### 3. **PromoPolska** 💰
Local deals and coupons aggregator for Polish retailers
- **Tech**: Flask + React + Web Scraping
- **Monetization**: Ad-supported
- **Ports**: Backend 8003, Frontend 3003
- **Features**: Deal aggregation, price tracking, favorite stores

### 4. **CenWatch PL** 📉
Price drop tracker for Polish e-commerce sites
- **Tech**: Flask + React + Redis
- **Monetization**: Freemium
- **Ports**: Backend 8004, Frontend 3004
- **Features**: Price monitoring, alerts, price history graphs

### 5. **DarmoSwap** 🔄
Free item exchange platform promoting reuse
- **Tech**: Django + React + PostgreSQL
- **Monetization**: Ad-supported
- **Ports**: Backend 8005, Frontend 3005
- **Features**: Listings, location-based search, image uploads

### 6. **Działkowiec Planner** 🌱
Allotment garden scheduler for Polish climate
- **Tech**: Flask + React PWA
- **Monetization**: One-time purchase
- **Ports**: Backend 8006, Frontend 3006
- **Features**: Planting calendar, reminders, offline support

### 7. **PupilCare** 🐕
Pet health scheduler for Polish pet owners
- **Tech**: Flask + React
- **Monetization**: One-time purchase
- **Ports**: Backend 8007, Frontend 3007
- **Features**: Pet profiles, vaccination tracking, Polish vet guidelines

### 8. **Dokumentownik** 📄
Personal document expiry tracker
- **Tech**: Flask + React
- **Monetization**: Ad-supported
- **Ports**: Backend 8008, Frontend 3008
- **Features**: Document vault, expiry alerts, Polish document types

### 9. **EventRadar Polska** 🎉
Local events aggregator for Polish cities
- **Tech**: Flask + React + Web Scraping
- **Monetization**: Ad-supported
- **Ports**: Backend 8009, Frontend 3009
- **Features**: Event aggregation, search, user reminders

### 10. **PolishWriter** ✍️
Grammar and style assistant for Polish language
- **Tech**: Flask + React + NLP
- **Monetization**: Subscription
- **Ports**: Backend 8010, Frontend 3010
- **Features**: Grammar check, style suggestions, LanguageTool integration

## 📁 Project Structure

```
polish-saas/
├── apps/                           # All 10 SaaS applications
│   ├── imieniny-reminder/
│   │   ├── backend/               # Django backend
│   │   ├── frontend/              # Next.js frontend
│   │   └── README.md
│   ├── airaware-polska/
│   │   ├── backend/               # FastAPI backend
│   │   ├── frontend/              # Next.js frontend
│   │   └── README.md
│   └── ... (8 more apps)
├── packages/                       # Shared packages
│   ├── shared-ui/                 # Reusable React components
│   │   ├── components/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Spinner.tsx
│   │   └── package.json
│   └── shared-utils/              # Utility functions
│       ├── api.ts                 # API client
│       ├── formatters.ts          # Polish formatters
│       ├── validators.ts          # Polish validators
│       └── package.json
├── scripts/                        # Development scripts
│   ├── generate-app-structure.py
│   ├── install-all.sh
│   └── dev-all.sh
├── docker-compose.yml             # Docker orchestration
├── package.json                   # Root workspace config
├── README.md
└── CONTRIBUTING.md
```

## 🛠️ Tech Stack

### Frontend (All Apps)
- **Framework**: Next.js 14 with React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Heroicons
- **HTTP Client**: Axios
- **Build**: Webpack (via Next.js)

### Backend
- **Django Apps**: Imieniny Reminder, DarmoSwap
- **FastAPI Apps**: AirAware Polska
- **Flask Apps**: PromoPolska, CenWatch PL, Działkowiec Planner, PupilCare, Dokumentownik, EventRadar Polska, PolishWriter

### Infrastructure
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.11.x or higher
- **PostgreSQL** 15.x or higher
- **Redis** 7.x or higher
- **Docker & Docker Compose** (optional but recommended)

### Quick Start with Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd polish-saas
```

2. **Start all services**
```bash
docker-compose up
```

3. **Access the applications**
- Imieniny Reminder: http://localhost:3001
- AirAware Polska: http://localhost:3002
- PromoPolska: http://localhost:3003
- CenWatch PL: http://localhost:3004
- DarmoSwap: http://localhost:3005
- Działkowiec Planner: http://localhost:3006
- PupilCare: http://localhost:3007
- Dokumentownik: http://localhost:3008
- EventRadar Polska: http://localhost:3009
- PolishWriter: http://localhost:3010

### Manual Installation

1. **Install all dependencies**
```bash
./scripts/install-all.sh
```

2. **Set up environment variables**
```bash
# Copy .env.example to .env for each backend
for app in apps/*/backend; do
    [ -f "$app/.env.example" ] && cp "$app/.env.example" "$app/.env"
done
```

3. **Start PostgreSQL and Redis**
```bash
docker-compose up -d postgres redis
```

4. **Run database migrations**
```bash
# Django apps
cd apps/imieniny-reminder/backend
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser

cd ../../../apps/darmoswap/backend
source venv/bin/activate
python manage.py migrate
```

5. **Start all apps**
```bash
./scripts/dev-all.sh
```

### Individual App Development

To work on a single app:

```bash
# Frontend
cd apps/app-name/frontend
npm install
npm run dev

# Backend (Django)
cd apps/app-name/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver

# Backend (Flask)
cd apps/app-name/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Backend (FastAPI)
cd apps/app-name/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## 📚 Documentation

Each app has its own detailed README with:
- Feature descriptions
- API documentation
- Setup instructions
- Architecture notes

See individual app READMEs in `apps/*/README.md`

## 🧪 Testing

```bash
# Frontend tests
cd apps/app-name/frontend
npm run test

# Backend tests (Django)
cd apps/app-name/backend
python manage.py test

# Backend tests (Flask/FastAPI)
cd apps/app-name/backend
pytest
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start specific app
docker-compose up imieniny-reminder-backend imieniny-reminder-frontend

# View logs
docker-compose logs -f app-name

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up --build
```

## 💡 Development Tips

### Shared Components
Use shared UI components from `packages/shared-ui`:
```typescript
import { Button, Card, Input, Modal, Spinner } from '@polish-saas/shared-ui'
```

### Shared Utilities
Use utility functions from `packages/shared-utils`:
```typescript
import { ApiClient, formatDatePL, formatPLN, isValidEmail } from '@polish-saas/shared-utils'
```

### Adding a New Feature
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test locally
4. Commit: `git commit -m "feat: description"`
5. Push and create PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🌍 Polish Market Considerations

These apps are specifically designed for Polish users:

- **Language**: Full Polish language support (UI, content, documentation)
- **Locale**: Polish date/time formats, currency (PLN), phone numbers
- **Culture**: Name days, allotment gardens, Polish document types
- **Geography**: Polish cities, voivodeships, postal codes
- **Regulations**: GDPR compliance, Polish consumer protection laws
- **Payment**: Integration ready for Polish payment gateways (PayU, Przelewy24)

## 📊 Monetization Models

| App | Model | Details |
|-----|-------|---------|
| Imieniny Reminder | One-time purchase | Single payment for lifetime access |
| AirAware Polska | Freemium subscription | Free: 1 alert, Premium: unlimited |
| PromoPolska | Ad-supported | Banner ads, affiliate links |
| CenWatch PL | Freemium | Free: 3 items, Premium: unlimited |
| DarmoSwap | Ad-supported | Light ads, optional donations |
| Działkowiec Planner | One-time purchase | Pay once, use forever |
| PupilCare | One-time purchase | Single payment model |
| Dokumentownik | Ad-supported | Free with minimal ads |
| EventRadar Polska | Ad-supported | Event promotions, banners |
| PolishWriter | Subscription | Monthly premium plan |

## 🚢 Deployment

### Production Deployment

1. **Build all apps**
```bash
npm run build
```

2. **Set up production environment**
```bash
# Set production environment variables
export NODE_ENV=production
export DATABASE_URL=postgresql://...
export REDIS_URL=redis://...
```

3. **Deploy with Docker**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Cloud Platforms

The monorepo is ready to deploy to:
- **Vercel** (frontends)
- **Railway** (backends)
- **Heroku** (all-in-one)
- **DigitalOcean App Platform**
- **AWS ECS**
- **Google Cloud Run**

## 📈 Roadmap

- [ ] Add payment integrations (Stripe, PayU)
- [ ] Mobile apps (React Native)
- [ ] Advanced analytics dashboards
- [ ] Multi-language support (English, German)
- [ ] SEO optimization for all apps
- [ ] Performance monitoring (Sentry)
- [ ] A/B testing framework
- [ ] Marketing websites for each app

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📝 License

MIT License - see LICENSE for details

## 🙏 Acknowledgments

- Built for the Polish market with ❤️
- Inspired by real needs of Polish consumers
- Data sources: GIOŚ, OpenAQ, Polish government APIs

## 📧 Contact

For questions or support, please open an issue or contact the maintainers.

---

**Built with 🇵🇱 for Poland**
