FROM python:3.11-slim

WORKDIR /app

COPY Kafka/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY Kafka/ .

CMD ["python", "main.py"]