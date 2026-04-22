"""
WSGI entry point for production servers (Gunicorn, Waitress, etc.)
Usage: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""
import sys
from server import app

if __name__ == "__main__":
    app.run()
