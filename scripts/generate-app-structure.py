#!/usr/bin/env python3
"""
Script to generate boilerplate structure for Polish SaaS apps
"""
import os
import json
from pathlib import Path

APPS_CONFIG = {
    "promo-polska": {
        "name": "PromoPolska",
        "description": "Local deals and coupons aggregator for Polish retailers",
        "backend_type": "flask",
        "port_backend": 8003,
        "port_frontend": 3003,
        "features": ["web_scraping", "deals_aggregation", "user_favorites"],
    },
    "cenwatch-pl": {
        "name": "CenWatch PL",
        "description": "Price drop tracker for Polish e-commerce sites",
        "backend_type": "flask",
        "port_backend": 8004,
        "port_frontend": 3004,
        "features": ["price_tracking", "price_history", "alerts"],
    },
    "darmoswap": {
        "name": "DarmoSwap",
        "description": "Free item exchange platform for Polish users",
        "backend_type": "django",
        "port_backend": 8005,
        "port_frontend": 3005,
        "features": ["listings", "user_accounts", "location_based"],
    },
    "dzialkowiec-planner": {
        "name": "Działkowiec Planner",
        "description": "Allotment garden scheduler for Polish climate",
        "backend_type": "flask",
        "port_backend": 8006,
        "port_frontend": 3006,
        "features": ["planting_calendar", "reminders", "plant_database"],
    },
    "pupilcare": {
        "name": "PupilCare",
        "description": "Pet health scheduler for Polish pet owners",
        "backend_type": "flask",
        "port_backend": 8007,
        "port_frontend": 3007,
        "features": ["pet_profiles", "vaccination_tracking", "reminders"],
    },
    "dokumentownik": {
        "name": "Dokumentownik",
        "description": "Personal document expiry tracker for Polish documents",
        "backend_type": "flask",
        "port_backend": 8008,
        "port_frontend": 3008,
        "features": ["document_storage", "expiry_alerts", "secure_vault"],
    },
    "eventradar-polska": {
        "name": "EventRadar Polska",
        "description": "Local events aggregator for Polish cities",
        "backend_type": "flask",
        "port_backend": 8009,
        "port_frontend": 3009,
        "features": ["event_scraping", "event_search", "user_reminders"],
    },
    "polishwriter": {
        "name": "PolishWriter",
        "description": "Grammar and style assistant for Polish language",
        "backend_type": "flask",
        "port_backend": 8010,
        "port_frontend": 3010,
        "features": ["nlp", "grammar_check", "style_suggestions"],
    },
}


def create_flask_backend(app_path, config):
    """Create Flask backend structure"""
    backend_path = app_path / "backend"
    backend_path.mkdir(parents=True, exist_ok=True)

    # requirements.txt
    requirements = """flask==3.0.0
flask-cors==4.0.0
flask-sqlalchemy==3.1.1
flask-jwt-extended==4.6.0
psycopg2-binary==2.9.9
python-decouple==3.8
celery==5.3.6
redis==5.0.1
requests==2.31.0
beautifulsoup4==4.12.3
gunicorn==21.2.0
"""
    (backend_path / "requirements.txt").write_text(requirements)

    # app.py
    app_code = f"""from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from decouple import config

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL', default='sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY', default='change-this-in-production')

db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    return jsonify({{
        'message': 'Welcome to {config["name"]} API',
        'status': 'operational'
    }})

@app.route('/health')
def health():
    return jsonify({{'status': 'healthy'}})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port={config["port_backend"]})
"""
    (backend_path / "app.py").write_text(app_code)

    # Dockerfile
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
"""
    (backend_path / "Dockerfile").write_text(dockerfile)

    # .env.example
    env_example = f"""DATABASE_URL=postgresql://postgres:postgres@localhost:5432/{app_path.name}
JWT_SECRET_KEY=change-this-in-production
REDIS_URL=redis://localhost:6379/0
"""
    (backend_path / ".env.example").write_text(env_example)

    print(f"✓ Created Flask backend for {config['name']}")


def create_react_frontend(app_path, config):
    """Create React/Next.js frontend structure"""
    frontend_path = app_path / "frontend"
    frontend_path.mkdir(parents=True, exist_ok=True)

    # package.json
    package_json = {
        "name": f"@polish-saas/{app_path.name}-frontend",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": f"next dev -p {config['port_frontend']}",
            "build": "next build",
            "start": f"next start -p {config['port_frontend']}",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "^14.1.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "axios": "^1.6.5",
            "@headlessui/react": "^1.7.18",
            "@heroicons/react": "^2.1.1"
        },
        "devDependencies": {
            "@types/node": "^20.11.5",
            "@types/react": "^18.2.48",
            "@types/react-dom": "^18.2.18",
            "typescript": "^5.3.3",
            "autoprefixer": "^10.4.17",
            "postcss": "^8.4.33",
            "tailwindcss": "^3.4.1",
            "eslint": "^8.56.0",
            "eslint-config-next": "^14.1.0"
        }
    }
    (frontend_path / "package.json").write_text(json.dumps(package_json, indent=2))

    # Create src/app directory
    app_dir = frontend_path / "src" / "app"
    app_dir.mkdir(parents=True, exist_ok=True)

    # page.tsx
    page_tsx = f"""'use client'

import {{ useState, useEffect }} from 'react'

export default function Home() {{
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            {config['name']}
          </h1>
          <p className="text-gray-600 mt-2">
            {config['description']}
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Witamy w {config['name']}!
          </h2>
          <p className="text-gray-600">
            Aplikacja w fazie rozwoju. Wkrótce dostępne nowe funkcje.
          </p>
        </div>
      </div>
    </main>
  )
}}
"""
    (app_dir / "page.tsx").write_text(page_tsx)

    # layout.tsx
    layout_tsx = f"""import type {{ Metadata }} from 'next'
import {{ Inter }} from 'next/font/google'
import './globals.css'

const inter = Inter({{ subsets: ['latin'] }})

export const metadata: Metadata = {{
  title: '{config["name"]} - {config["description"]}',
  description: '{config["description"]}',
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="pl">
      <body className={{inter.className}}>{{children}}</body>
    </html>
  )
}}
"""
    (app_dir / "layout.tsx").write_text(layout_tsx)

    # globals.css
    globals_css = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
    (app_dir / "globals.css").write_text(globals_css)

    print(f"✓ Created React frontend for {config['name']}")


def create_readme(app_path, config):
    """Create README for the app"""
    readme = f"""# {config['name']}

{config['description']}

## Features

{chr(10).join([f'- {feature.replace("_", " ").title()}' for feature in config['features']])}

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

Visit http://localhost:{config['port_frontend']}

## License

MIT
"""
    (app_path / "README.md").write_text(readme)
    print(f"✓ Created README for {config['name']}")


def main():
    base_path = Path(__file__).parent.parent / "apps"

    for app_slug, config in APPS_CONFIG.items():
        app_path = base_path / app_slug
        print(f"\nGenerating {config['name']}...")

        # Create backend
        if config["backend_type"] == "flask":
            create_flask_backend(app_path, config)

        # Create frontend
        create_react_frontend(app_path, config)

        # Create README
        create_readme(app_path, config)

        print(f"✓ {config['name']} generated successfully!\n")

    print("\n" + "="*50)
    print("All apps generated successfully!")
    print("="*50)


if __name__ == "__main__":
    main()
