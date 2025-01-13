#!/bin/bash

# Delete all .pyc files
find . -name "*.pyc" -type f -delete

# Fetch all processes using port 8888 and kill them
PIDS=$(lsof -t -i:8888)

if [ -n "$PIDS" ]; then
    echo "Killing the following processes on port 8888: $PIDS"
    kill -9 $PIDS
else
    echo "No processes found on port 8888."
fi
