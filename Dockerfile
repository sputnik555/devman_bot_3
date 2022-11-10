# syntax=docker/dockerfile:1
FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY *.py .
COPY *.json .

CMD [ "python3", "tg_bot.py"]