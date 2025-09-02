FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
# COPY your chains/server code to /app and run uvicorn (example):
# COPY app /app/app
# CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8080"]
EXPOSE 8080
