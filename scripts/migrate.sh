export CONTAINER_NAME="hackclub_backend"
docker exec -it $CONTAINER_NAME alembic upgrade head
