# ---------------------------------------------
# COMPILER
# ---------------------------------------------

FROM docker.io/library/python:3.11-slim AS compiler

USER root

WORKDIR /home/src

RUN pip install compile

COPY logic/ logic/
COPY app.py app.py

RUN python -m compile -b -f -o dist/ .
RUN rm -fr dist/env/


# ---------------------------------------------
# EXECUTION
# ---------------------------------------------

FROM docker.io/library/python:3.11-slim

USER root

ENV HOME=/home/jaime/master

RUN mkdir -p /home/src && chmod -R 777 /home/src && \
    mkdir -p /home/jaime && chmod -R 777 /home/jaime

WORKDIR /home/src

RUN apt-get update && \
    apt-get install iputils-ping curl git wget procps -y

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm -fr requirements.txt

COPY --from=compiler /home/src/dist/ .
COPY logic/resources/ logic/resources/

USER 1001

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV JAIME_HOME_PATH=/home/jaime/master/
ENV WORKINGDIR_PATH=/home/jaime/workingdir/
ENV STORAGE_PATH=/home/jaime/storage/
ENV TZ=America/Argentina/Buenos_Aires

EXPOSE 5000

CMD ["/bin/bash", "-c", "python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=6 app:app"]
