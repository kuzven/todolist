#!/bin/sh

echo "Waiting for web to become available..."
while ! nc -z web 8000; do
  sleep 1
done

echo "Web is available. Starting Nginx."
exec "$@"
