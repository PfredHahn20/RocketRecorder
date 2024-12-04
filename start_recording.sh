#!/bin/bash

LOG_FILE="/home/pi/logs/start_recording.log"
exec > $LOG_FILE 2>&1

# Find the highest existing video number and increment it
LAST_FILE=$(ls /home/pi/video_*.h264 2>/dev/null | sort | tail -n 1)
if [ -z "$LAST_FILE" ]; then
        NEXT_NUM=0001
else
        LAST_NUM=$(basename "$LAST_FILE" .h264 | sed 's/video_//')
        NEXT_NUM=$(printf "%04d" $((10#$LAST_NUM + 1)))
fi

CONTROL_FILE="/home/pi/stop_recording"
rm -f "$CONTROL_FILE"


libcamera-vid -t 0 -o /home/pi/video_$NEXT_NUM.h264 &
VID_PID=$!
echo $VID_PID > /home/pi/recording_pid
echo "Recording started with PID: $VID_PID"

while [ ! -f "$CONTROL_FILE" ]; do
        sleep 1
done

echo "Stopping recording with PID: $VID_PID"
kill -2 $VID_PID
rm -f "$CONTROL_FILE"
echo "Recording Stopped (from start_recording shell script)"
