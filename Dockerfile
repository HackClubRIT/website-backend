FROM python:3.8.1-slim

RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential libpq-dev python-psycopg2 gcc \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

COPY . ./src

WORKDIR /src

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]