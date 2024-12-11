#!/bin/bash

# Start Flask App
flask run --host=0.0.0.0 &

# Start Nginx
nginx -g 'daemon off;'
