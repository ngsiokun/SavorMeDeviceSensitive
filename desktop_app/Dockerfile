# Dockerfile for SavorMe Desktop Frontend
# Optimized for desktop screens (1024px+)

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy desktop app files
COPY requirements.txt .
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV BACKEND_URL=http://127.0.0.1:8000

# Expose port
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

