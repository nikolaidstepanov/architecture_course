#!/bin/bash

ENDPOINT="http://localhost:8000/rand_metrics"
DURATION=60
START_TIME=$(date +%s)
COUNT=0

echo "Sending requests to $ENDPOINT for $DURATION seconds..."

while [ $(($(date +%s) - $START_TIME)) -lt $DURATION ]; do
  RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)
  if [ "$RESPONSE" -eq 200 ]; then
    echo "Request #$((++COUNT)): Success"
  else
    echo "Request #$((++COUNT)): Failed with status code $RESPONSE"
  fi
  sleep 1  # Adjust this delay to control request frequency
done

echo "Total requests sent: $COUNT"