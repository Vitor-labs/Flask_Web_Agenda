FROM python:3.8.12-bullseye

WORKDIR /app

COPY requisitos.txt .

RUN pip install -r requisitos.txt

EXPOSE 5000

ENV FLASK_ENV development

COPY app.py .

