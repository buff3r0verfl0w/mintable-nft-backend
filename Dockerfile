FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install --upgrade --no-cache-dir -r requirements.txt

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
