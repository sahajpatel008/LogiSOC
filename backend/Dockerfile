FROM python:3.11.5-slim

WORKDIR /flask_app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
