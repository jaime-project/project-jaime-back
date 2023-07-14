# COMPILER
# ---------------------------------------------
FROM python:3.10-slim as compiler

USER root

WORKDIR /home/jaime

RUN pip install compile

COPY logic/ logic/
COPY app.py app.py

RUN python -m compile -b -f -o dist/ .
RUN rm -fr dist/repo_modules_default

# EXECUTION
# ---------------------------------------------
FROM python:3.10-slim

WORKDIR /home/jaime

USER root

RUN apt-get update
RUN apt-get install iputils-ping curl git wget procps -y

COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN rm -fr requirements.txt

RUN useradd -ms /bin/bash -d /home/jaime 1001
RUN chown -R 1001:0 /home/jaime
RUN chmod -R 777 /home/jaime
USER 1001

RUN mkdir -p .jaime/ .shared/workingdir/

COPY --from=compiler /home/jaime/dist/ ./
COPY logic/resources logic/resources

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=5000
ENV JAIME_HOME_PATH=/home/jaime/.jaime/
ENV WORKINGDIR_PATH=/home/jaime/.shared/workingdir/
ENV TZ=America/Argentina/Buenos_Aires

CMD python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=6 app:app

EXPOSE 5000
