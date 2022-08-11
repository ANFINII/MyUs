FROM python:3.9.7-alpine
ENV PYHONUNBUFFERED 1
WORKDIR /api
COPY /requirements /requirements
RUN pip install -r /requirements/dev.txt
