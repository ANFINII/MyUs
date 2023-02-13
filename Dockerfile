FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /backend

WORKDIR /backend

RUN apt update \
    && apt-get -y install gcc libmariadb-dev \
    && apt install -y default-mysql-client \
    && apt-get install -y default-libmysqlclient-dev \
    && apt install --no-install-recommends -y tzdata \
    && apt-get install -y git \
    && apt clean

COPY /backend/requirements /backend/requirements
RUN pip install --upgrade pip
RUN pip install -r /backend/requirements/dev.txt

# COPY ./entrypoint /entrypoint
# RUN sed -i 's/\r$//g' /entrypoint
# RUN chmod +x /entrypoint

ADD . /backend

EXPOSE 8056
# ENTRYPOINT ["/entrypoint"]
# CMD cd /backend && uvicorn app.main:app --reload --port=$PORT --host=0.0.0.0 --log-level debug
# CMD [ "uwsgi", "--http", ":80", "--module", "config.wsgi", "config.asgi" ]
CMD [ "uwsgi", "--http", ":80", "--module", "config.wsgi" ]
