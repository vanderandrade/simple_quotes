FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get install -y python-pip python-dev python-psycopg2 postgresql-client

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt
CMD ["./run.sh"]