FROM python:slim as base
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code
WORKDIR /code/
RUN rm venv -rf
RUN pip install -r requirements.txt --no-cache-dir

FROM base as tests
RUN pip install -r tests/test_requirements.txt --no-cache-dir
RUN ["sh", "run_tests.sh"]

FROM tests as production
RUN pip uninstall -r tests/test_requirements.txt --no-cache-dir -y
RUN rm tests -rf