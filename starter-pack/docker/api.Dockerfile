
# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# Python deps
COPY app/requirements.txt /app/app/requirements.txt
RUN pip install --no-cache-dir -r /app/app/requirements.txt

# App
COPY app /app/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
