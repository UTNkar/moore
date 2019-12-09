FROM python:3.5

ENV PYTHONUNBUFFERED 1
WORKDIR /var/www/moore
RUN pip install -r requirements.txt