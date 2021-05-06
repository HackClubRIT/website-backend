SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
. $SCRIPTPATH/set_env.sh

docker exec -it $CONTAINER_NAME pylint app