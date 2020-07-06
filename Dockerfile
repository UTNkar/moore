FROM python:3.8

ENV PYTHONUNBUFFERED 1
WORKDIR /var/www/moore
COPY requirements.txt .
COPY dev-requirements.txt .
RUN pip install -r dev-requirements.txt
