#!/bin/bash

echo "Installing Polish SaaS Monorepo Dependencies"
echo "=============================================="

# Install root dependencies
echo "Installing root dependencies..."
npm install

# Install frontend dependencies for all apps
for app in apps/*/frontend; do
    if [ -d "$app" ]; then
        echo "Installing dependencies for $app..."
        (cd "$app" && npm install)
    fi
done

# Install Python dependencies for all apps
for app in apps/*/backend; do
    if [ -d "$app" ] && [ -f "$app/requirements.txt" ]; then
        echo "Setting up Python environment for $app..."
        (cd "$app" && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt)
    fi
done

echo ""
echo "✓ All dependencies installed successfully!"
echo ""
echo "Next steps:"
echo "1. Set up PostgreSQL and Redis"
echo "2. Copy .env.example files to .env in each backend directory"
echo "3. Run migrations for Django apps"
echo "4. Use 'docker-compose up' to start all services"
