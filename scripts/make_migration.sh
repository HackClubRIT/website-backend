SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
. $SCRIPTPATH/set_env.sh
if [ -z "$1" ]
then
   echo "ERROR: Empty Message";
else
  docker exec -it $CONTAINER_NAME alembic revision -m $1
fi

