#!/bin/bash
# Migrate
alembic upgrade head
# Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 80