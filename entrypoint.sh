#!/bin/bash
# Migrate
alembic upgrade head
# Run
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-80}