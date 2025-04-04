# ---------------------------------------------
# COMPILER
# ---------------------------------------------
FROM docker.io/library/python:3.12-slim AS compiler

WORKDIR /home/src

USER root

RUN apt update && \
    apt install -y binutils

COPY . .
RUN pip install -r requirements.txt

RUN pyinstaller --add-data logic:logic -n jaime --onefile app.py


# ---------------------------------------------
# FINAL IMAGE
# ---------------------------------------------
FROM docker.io/library/ubuntu:24.04

ARG ARG_VERSION=local

WORKDIR /home/jaime

USER root

RUN apt-get update && \
    apt-get install -y iputils-ping curl git wget procps 

COPY --from=compiler /home/src/dist/jaime /usr/local/bin/jaime
RUN chmod +x /usr/local/bin/jaime && \
    chmod 770 /home/jaime -R

ENV HOME=/home/jaime

USER 1001

ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV VERSION=${ARG_VERSION}
ENV JAIME_HOME_PATH=/home/jaime/master/
ENV WORKINGDIR_PATH=/home/jaime/workindir/
ENV STORAGE_PATH=/home/jaime/storage/
# ENV TZ=America/Argentina/Buenos_Aires

EXPOSE 5000

CMD ["/usr/local/bin/jaime"]
