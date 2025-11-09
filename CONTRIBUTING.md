# Contributing to Polish SaaS Monorepo

Thank you for your interest in contributing to this project!

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start

1. Clone the repository
```bash
git clone <repository-url>
cd polish-saas
```

2. Install all dependencies
```bash
./scripts/install-all.sh
```

3. Set up environment variables
```bash
# Copy .env.example to .env for each backend
for app in apps/*/backend; do
    cp "$app/.env.example" "$app/.env"
done
```

4. Start services with Docker Compose
```bash
docker-compose up -d postgres redis
```

5. Run migrations for Django apps
```bash
cd apps/imieniny-reminder/backend
source venv/bin/activate
python manage.py migrate

cd ../../../apps/darmoswap/backend
source venv/bin/activate
python manage.py migrate
```

6. Start all apps in development mode
```bash
./scripts/dev-all.sh
```

## Project Structure

```
polish-saas/
├── apps/              # All 10 SaaS applications
│   ├── app-name/
│   │   ├── backend/   # Python backend (Django/Flask/FastAPI)
│   │   ├── frontend/  # Next.js frontend
│   │   └── README.md
├── packages/          # Shared packages
│   ├── shared-ui/     # Reusable UI components
│   └── shared-utils/  # Utility functions
├── scripts/           # Development scripts
└── docker-compose.yml
```

## Code Style

### TypeScript/JavaScript

- Use TypeScript for all new code
- Follow ESLint rules
- Use Prettier for formatting
- Prefer functional components with hooks

### Python

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all functions
- Use Black for formatting

## Adding a New Feature

1. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes

3. Test your changes locally

4. Commit with a clear message
```bash
git commit -m "feat: add new feature description"
```

5. Push and create a pull request

## Commit Message Format

Follow the Conventional Commits specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Testing

### Frontend
```bash
cd apps/app-name/frontend
npm run test
```

### Backend
```bash
cd apps/app-name/backend
source venv/bin/activate
pytest
```

## Documentation

- Update README.md when adding new features
- Document all API endpoints
- Add JSDoc comments for TypeScript functions
- Write docstrings for Python functions

## Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing! 🎉
