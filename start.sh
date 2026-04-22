#!/bin/bash
PORT=${PORT:-5000}
gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:app
