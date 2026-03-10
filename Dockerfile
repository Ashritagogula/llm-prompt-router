FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run interactive script (this might need to be run with `-it` via docker)
CMD ["python", "app.py"]
