#!/bin/bash

LOCAL_DUMP_PATH=$1
REMOTE_DUMP_PATH="/var/tmp/dump.sql"

docker cp $LOCAL_DUMP_PATH moore-db:$REMOTE_DUMP_PATH
docker exec -it moore-db dropdb -U moore moore
docker exec -it moore-db createdb -U moore moore
docker exec -it moore-db psql -U moore -d moore -f $REMOTE_DUMP_PATH
docker exec -it moore-db rm -f $REMOTE_DUMP_PATH