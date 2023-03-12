FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /code

RUN mkdir /code
WORKDIR /code

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y default-libmysqlclient-dev \
  && apt-get install -y git \
  && apt-get install -y libgraphviz-dev graphviz pkg-config \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY /backend/requirements /code/requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements/dev.txt

ADD . /code/
EXPOSE 8056

# CMD cd /backend && uvicorn app.main:app --reload --port=$PORT --host=0.0.0.0 --log-level debug
