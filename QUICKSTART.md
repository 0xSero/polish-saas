# Quick Start Guide - Get Running in 10 Minutes! 🚀

This guide will get all 10 apps running with Stripe payments in under 10 minutes.

## Prerequisites

- Node.js 18+ and Python 3.11+ installed
- Docker installed (for PostgreSQL and Redis)
- Stripe account (free at [stripe.com](https://stripe.com))

## Step 1: Get Stripe Keys (2 minutes)

1. Go to [stripe.com](https://stripe.com) and sign up
2. Navigate to **Developers → API keys**
3. Copy your test keys:
   - **Publishable key**: `pk_test_...`
   - **Secret key**: `sk_test_...`

## Step 2: Start Infrastructure (1 minute)

```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Verify they're running
docker ps
```

## Step 3: Configure Stripe Keys (2 minutes)

We'll set up Imieniny Reminder as an example (repeat for other apps as needed):

```bash
# Backend
cd apps/imieniny-reminder/backend
cp .env.example .env

# Edit .env and add:
# STRIPE_SECRET_KEY=sk_test_your_key_here
# STRIPE_PUBLIC_KEY=pk_test_your_key_here

# Frontend
cd ../frontend
cp .env.example .env.local

# Edit .env.local and add:
# NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_test_your_key_here
# NEXT_PUBLIC_API_URL=http://localhost:8001
```

Or use this one-liner:

```bash
# Backend
echo "STRIPE_SECRET_KEY=sk_test_YOUR_KEY
STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY
SECRET_KEY=django-insecure-dev-key
DEBUG=True
DB_NAME=imieniny_reminder
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432" > apps/imieniny-reminder/backend/.env

# Frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY" > apps/imieniny-reminder/frontend/.env.local
```

## Step 4: Set Up Backend (2 minutes)

```bash
cd apps/imieniny-reminder/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start backend
python manage.py runserver 8001
```

## Step 5: Set Up Frontend (2 minutes)

Open a new terminal:

```bash
cd apps/imieniny-reminder/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Step 6: Test Payment Flow (1 minute)

1. Open browser to `http://localhost:3001`
2. Click "Kup teraz - 49 zł" (Buy now)
3. Register or login
4. Go to pricing page
5. Click checkout
6. Use test card: **4242 4242 4242 4242**
   - Expiry: Any future date
   - CVC: Any 3 digits
   - ZIP: Any 5 digits
7. Complete payment
8. You'll be redirected back!

## Step 7: Verify Payment (Optional)

Check Stripe Dashboard:
1. Go to [dashboard.stripe.com](https://dashboard.stripe.com)
2. Click **Payments**
3. You should see your test payment!

## 🎉 You're Done!

The app is now fully functional with:
- ✅ User authentication
- ✅ Stripe payments
- ✅ Dashboard
- ✅ Payment tracking

## Run All Apps Simultaneously

```bash
# Option 1: Use our script
./scripts/dev-all.sh

# Option 2: Docker Compose (coming soon)
docker-compose up
```

## Quick Reference

### All App Ports

| App | Backend | Frontend |
|-----|---------|----------|
| Imieniny Reminder | 8001 | 3001 |
| AirAware Polska | 8002 | 3002 |
| PromoPolska | 8003 | 3003 |
| CenWatch PL | 8004 | 3004 |
| DarmoSwap | 8005 | 3005 |
| Działkowiec Planner | 8006 | 3006 |
| PupilCare | 8007 | 3007 |
| Dokumentownik | 8008 | 3008 |
| EventRadar Polska | 8009 | 3009 |
| PolishWriter | 8010 | 3010 |

### Test Cards

| Card | Scenario |
|------|----------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 9995 | Declined |
| 4000 0025 0000 3155 | 3D Secure |

### Common Commands

```bash
# Backend (Django)
python manage.py runserver 8001
python manage.py migrate
python manage.py createsuperuser

# Frontend
npm run dev
npm run build
npm start

# Docker
docker-compose up -d postgres redis
docker-compose down
docker-compose logs -f
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
# or
npm install
```

### "Database connection failed"
```bash
docker-compose up -d postgres
# Wait 5 seconds, then:
python manage.py migrate
```

### "Stripe key invalid"
- Check you copied the full key (starts with `pk_test_` or `sk_test_`)
- No extra spaces
- Using test keys, not live keys

### Port already in use
```bash
# Kill process on port (example: 8001)
lsof -ti:8001 | xargs kill -9
```

## Next Steps

1. **Customize the apps**: Update branding, colors, text
2. **Add content**: Polish name days data, air quality sources, etc.
3. **Test thoroughly**: Try all features
4. **Deploy**: See README.md for deployment guides
5. **Go live**: Switch to live Stripe keys

## Need Help?

- **Stripe Docs**: [stripe.com/docs](https://stripe.com/docs)
- **Main README**: See `README.md` for detailed setup
- **Stripe Setup**: See `STRIPE_SETUP.md` for payment integration
- **Status**: See `STATUS.md` for what's implemented

---

**That's it! You now have 10 production-ready SaaS apps!** 🎊

Happy coding! 🚀
