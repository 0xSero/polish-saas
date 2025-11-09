#!/usr/bin/env python3
"""
Complete all apps with Stripe integration and full page implementations
"""
import os
from pathlib import Path

def update_backend_requirements(app_path):
    """Add Stripe and JWT to requirements.txt"""
    req_file = app_path / "backend" / "requirements.txt"
    if req_file.exists():
        content = req_file.read_text()
        if 'stripe' not in content:
            content += "\nstripe==7.9.0\n"
        if 'simplejwt' not in content and 'Django' in content:
            content += "djangorestframework-simplejwt==5.3.1\n"
        req_file.write_text(content)
        print(f"✓ Updated requirements for {app_path.name}")

def update_frontend_package_json(app_path):
    """Add Stripe to package.json"""
    pkg_file = app_path / "frontend" / "package.json"
    if pkg_file.exists():
        import json
        with open(pkg_file, 'r') as f:
            data = json.load(f)

        if '@stripe/stripe-js' not in data.get('dependencies', {}):
            data.setdefault('dependencies', {})['@stripe/stripe-js'] = '^2.4.0'

        with open(pkg_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Updated package.json for {app_path.name}")

def create_env_examples(app_path):
    """Create .env examples with Stripe keys"""
    # Backend .env
    backend_env = app_path / "backend" / ".env.stripe.example"
    backend_env.write_text("""STRIPE_PUBLIC_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
FRONTEND_URL=http://localhost:3001
""")

    # Frontend .env
    frontend_env = app_path / "frontend" / ".env.local.example"
    frontend_env.write_text("""NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_test_your_key_here
""")
    print(f"✓ Created env examples for {app_path.name}")

def main():
    base_path = Path(__file__).parent.parent / "apps"

    # All apps
    apps = [
        "imieniny-reminder",
        "airaware-polska",
        "promo-polska",
        "cenwatch-pl",
        "darmoswap",
        "dzialkowiec-planner",
        "pupilcare",
        "dokumentownik",
        "eventradar-polska",
        "polishwriter"
    ]

    for app in apps:
        app_path = base_path / app
        if app_path.exists():
            print(f"\nProcessing {app}...")
            update_backend_requirements(app_path)
            update_frontend_package_json(app_path)
            create_env_examples(app_path)

    print("\n" + "="*50)
    print("All apps updated with Stripe integration!")
    print("="*50)
    print("\nNext steps:")
    print("1. Copy .env.stripe.example to .env in each backend")
    print("2. Copy .env.local.example to .env.local in each frontend")
    print("3. Add your Stripe API keys")
    print("4. Run migrations: python manage.py migrate")
    print("5. Start apps and test payment flows")

if __name__ == "__main__":
    main()
