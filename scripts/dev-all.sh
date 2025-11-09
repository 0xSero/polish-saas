#!/bin/bash

echo "Starting all Polish SaaS apps in development mode..."
echo "======================================================"

# Array to store background process PIDs
pids=()

# Start all backends
for app in apps/*/backend; do
    if [ -d "$app" ]; then
        app_name=$(basename $(dirname "$app"))
        echo "Starting backend for $app_name..."

        if [ -f "$app/manage.py" ]; then
            # Django app
            (cd "$app" && source venv/bin/activate && python manage.py runserver) &
        elif [ -f "$app/app.py" ]; then
            # Flask app
            (cd "$app" && source venv/bin/activate && python app.py) &
        elif [ -f "$app/main.py" ]; then
            # FastAPI app
            (cd "$app" && source venv/bin/activate && uvicorn main:app --reload) &
        fi

        pids+=($!)
    fi
done

# Start all frontends
for app in apps/*/frontend; do
    if [ -d "$app" ]; then
        app_name=$(basename $(dirname "$app"))
        echo "Starting frontend for $app_name..."
        (cd "$app" && npm run dev) &
        pids+=($!)
    fi
done

echo ""
echo "All apps started!"
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap 'echo "Stopping all services..."; kill ${pids[@]}; exit' INT

# Keep script running
wait
