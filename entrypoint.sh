#!/bin/bash
while true; do
    python weather_service.py
    echo "Process failed with exit code $?. Sleeping for 10 seconds..."
    sleep 60
done 