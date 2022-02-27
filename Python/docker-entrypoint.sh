#!/bin/bash

set -e

echo "Initial check DB connection started..."

RES=$(python check_conn.py)

if [ "$RES" !=  'Connection to PG is active.' ]; then
   echo "DB server is not available"
   echo "Termination..."
   exit 1
else
   exec python geninfo.py
fi
