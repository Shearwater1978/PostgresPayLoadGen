#!/bin/bash

set -e

if [ "$SEND_TO_CONSOLE" == 'False' ]; then
   echo "Initial check DB connection started..."
   RES=$(python check_conn.py)
fi

if [ "$SEND_TO_CONSOLE" == 'True' ]; then
   echo "Check env variables"
   echo "BEHAVIOR_MODEL: $BEHAVIOR_MODEL"
   echo "SEND_TO_API: $SEND_TO_API"
   echo "API_ENDPOINT: $API_ENDPOINT"
   echo "RANDOM_FACTOR: $RANDOM_FACTOR"
   echo "CYCLIAL_MODE: $CYCLIAL_MODE"
   echo "PERSON_COUNT: $PERSON_COUNT"
   exec python geninfo.py
else
   if [ "$RES" !=  'Connection to PG is active.' ]; then
      echo "DB server is not available"
      echo "Termination..."
      exit 1
   else
      while :
      do
         echo "Run send payload in cyclial mode..."
         python geninfo.py
      done
   fi
fi