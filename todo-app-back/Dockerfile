# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /application

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./application .

EXPOSE 5000

RUN python3 -m flask db init

RUN python3 -m flask db migrate

RUN python3 -m flask db upgrade



CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]