FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-deps -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]