#!/bin/bash

# Initialize database
python -c "from app.database import init_db; init_db()"

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
