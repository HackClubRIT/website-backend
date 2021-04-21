CONTAINER_NAME="hackclub_backend"

if [ -z "$1" ]
then
   echo "ERROR: Empty Message";
else
  docker exec -it $CONTAINER_NAME alembic revision -m $1
fi

