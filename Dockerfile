FROM python:3.13-slim

WORKDIR /app

COPY manageTorrents.py ./manageTorrents.py
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "manageTorrents.py"]