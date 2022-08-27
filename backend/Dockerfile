FROM python:3.10.0

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /backend

COPY Pipfile Pipfile.lock /backend/

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # mysql dependencies
  && apt-get install -y default-libmysqlclient-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY /requirements /requirements
RUN pip install -r /requirements/dev.txt

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ADD . /admin/

ENTRYPOINT ["/entrypoint"]
EXPOSE 80

CMD [ "uwsgi", "--http", ":80", "--module", "config.wsgi" ]
