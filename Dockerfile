FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /srv/api
WORKDIR /srv/api
COPY requirements.txt /srv/api/
RUN pip install -r requirements.txt
COPY . /srv/api/

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]
