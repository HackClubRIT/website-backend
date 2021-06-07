FROM python:3.9.5-slim

ARG UID=1000
ARG GID=1000
ENV UNAME=docker

RUN groupadd -g $GID -o $UNAME && useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential libpq-dev python-psycopg2 gcc \
&& apt-get purge -y --auto-remove \
&& rm -rf /var/lib/apt/lists/*

COPY . ./src

WORKDIR /src

RUN pip install -r requirements.txt

RUN chown $UNAME /src && chmod +x ./entrypoint.sh

USER $UNAME

ENTRYPOINT ["./entrypoint.sh"]