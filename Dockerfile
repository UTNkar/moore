FROM python:3.5

ADD src/ /var/www/moore/src
WORKDIR /var/www/moore

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
