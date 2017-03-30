FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install -r requirements.txt
COPY . /src/

EXPOSE 5000
CMD ["python", "manage.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]
