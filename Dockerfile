FROM python:3.8.1-slim

RUN set -eux; \
	groupadd -r postgres --gid=999; \
	useradd -r -g postgres --uid=999 --home-dir=/var/lib/postgresql --shell=/bin/bash postgres; \
	mkdir -p /var/lib/postgresql; \
	chown -R postgres:postgres /var/lib/postgresql
RUN mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql && chmod 2777 /var/run/postgresql


RUN apt-get update \
&& apt-get install -y --no-install-recommends postgresql build-essential libpq-dev python-psycopg2 gcc \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

# Environment variables
ENV DB_USER='dbuser'
ENV DB_PASSWORD='password'
ENV DB_NAME='hackclubdb'
ENV DB_HOST='127.0.0.1'
ENV DB_PORT='5432'

# Create DB and User
USER postgres
RUN  service postgresql start \
&& psql -c "CREATE USER ${DB_USER} WITH SUPERUSER PASSWORD '${DB_PASSWORD}';ALTER USER ${DB_USER} CREATEDB;" \
&& psql -c "CREATE DATABASE ${DB_NAME} WITH owner ${DB_USER} encoding 'utf-8'"
USER root

COPY ./src /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["./startserver.sh"]