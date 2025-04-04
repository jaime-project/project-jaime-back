# ---------------------------------------------
# COMPILER
# ---------------------------------------------

FROM docker.io/library/python:3.12-slim AS compiler

USER root

WORKDIR /home/src

RUN pip install compile

COPY logic/ logic/
COPY app.py app.py

RUN python -m compile -b -f -o dist/ .
RUN rm -fr dist/env/


# ---------------------------------------------
# FINAL IMAGE
# ---------------------------------------------

FROM docker.io/library/python:3.12-slim

ARG ARG_VERSION=local

WORKDIR /home/src

USER root

ENV HOME=/home/jaime/master

RUN apt-get update && \
    apt-get install iputils-ping curl git wget procps -y

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm -fr requirements.txt

COPY --from=compiler /home/src/dist/ .
COPY logic/resources/ logic/resources/

RUN chmod 770 /home/src -R && chmod 770 /home/jaime -R

USER 1001

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV JAIME_HOME_PATH=/home/jaime/master/
ENV WORKINGDIR_PATH=/home/jaime/workingdir/
ENV STORAGE_PATH=/home/jaime/shared/
ENV TZ=America/Argentina/Buenos_Aires
ENV GUNICORN_WORKERS=1
ENV GUNICORN_THREADS=6

EXPOSE 5000

CMD ["/bin/bash", "-c", "python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=${GUNICORN_WORKERS} --threads=${GUNICORN_THREADS} app:app"]
