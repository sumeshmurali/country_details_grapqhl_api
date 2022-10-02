FROM python:slim as base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code
WORKDIR /code/
RUN rm tests -rf
RUN pip install -r requirements.txt --no-cache-dir