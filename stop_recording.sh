#!/bin/bash

LOG_FILE="/home/pi/logs/stop_recording.log"
exec > $LOG_FILE 2>&1

CONTROL_FILE="/home/pi/stop_recording"
PID=$(cat /home/pi/recording_pid)

if [ -n "$PID" ]; then
        echo "Stopping recording process with PID: $PID"
        touch "$CONTROL_FILE"
        sleep 1
        echo "Recording Stopped (from stop_recording shell script)"
else
        echo "No recording process found"
fi
