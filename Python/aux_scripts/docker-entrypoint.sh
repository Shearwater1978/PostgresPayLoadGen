#!/bin/bash

set -e

echo "Check env variables"
echo "CYCLIAL_MODE: $CYCLIAL_MODE"
echo "PERSON_COUNT: $PERSON_COUNT"
echo "DB_USER_NAME: $DB_USER_NAME"
echo "DB_USER_PASS: $DB_USER_PASS"
echo "DB_USER_DB: $DB_USER_DB"
echo "DB_USER_PG_HOST: $DB_USER_PG_HOST"
echo "DB_USER_PG_PORT: $DB_USER_PG_PORT"
echo "SEND_TO_CONSOLE: $SEND_TO_CONSOLE"


if [[ "$SEND_TO_CONSOLE" == 'False' ]]; then
   echo "Initial check DB connection started..."
   RES=`python check_conn.py`
   echo "${RES}"
fi

if [[ "$SEND_TO_CONSOLE" == 'True' ]]; then
   exec python new_persons_generator.py
else
   if [[ "$RES" != 'Connection to PG is active.' ]]; then
      echo "DB server is not available"
      echo "Termination..."
      exit 1
   else
      while :
      do
         echo "Run send payload in cyclial mode..."
         python new_persons_generator.py
      done
   fi
fi
