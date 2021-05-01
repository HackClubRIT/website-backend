#!/bin/bash
# Migrate
alembic upgrade head
# Run
if [ ${ALLOW_RELOAD:-"false"} = "true" ];
then
    echo "ALLOW_RELOAD"
    uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT:-80}
else
  uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-80}
fi