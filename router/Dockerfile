FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared models (will be copied from parent context)
COPY backend_app/shared/ ./shared/

# Copy service code
COPY main.py .

# Expose port (Cloud Run expects 8080)
EXPOSE 8080

# Run the service
CMD ["python", "main.py"]
