FROM python:3.5

ENV PYTHONUNBUFFERED 1
WORKDIR /var/www/moore
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt