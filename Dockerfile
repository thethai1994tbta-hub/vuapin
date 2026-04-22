FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application files
COPY server.py .
COPY index.html .
COPY admin.html .

# Create database directory
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_APP=server.py
ENV PYTHONUNBUFFERED=1

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "wsgi:app"]
