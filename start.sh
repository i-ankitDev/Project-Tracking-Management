#!/bin/bash

APPLICATION="main.py"
PID_HOME="/home/$USER/xbuild/.proc/tmp/marline"
LOG_FILE="/home/$USER/xbuild/server-start/log/run.log"

# Create the PID directory if it doesn't exist
mkdir -p $PID_HOME

# Define the Python version (assuming Python 3.x)
PYTHON_VERSION="3"

# Check if the application is already running
if pgrep -f "python$PYTHON_VERSION ./$APPLICATION" > /dev/null; then
    echo "$APPLICATION is already running."
    exit 1  # Exit if the process is already running
fi

# Start the application in the background using nohup
nohup python$PYTHON_VERSION ./$APPLICATION > $LOG_FILE 2>&1 &

# Get the PID of the started application
APPLICATION_PID=$!

# Save the PID to the PID file
echo $APPLICATION_PID > $PID_HOME/$APPLICATION.pid

echo "$APPLICATION started with PID $APPLICATION_PID"
