ARG ARG_VERSION local

# ---------------------------------------------
# COMPILER
# ---------------------------------------------

FROM docker.io/library/python:3.12-slim AS compiler

WORKDIR /home/src

USER root

COPY logic/ logic/
COPY app.py app.py

RUN pyinstaller --add-data logic:logic -n jaime --onefile app.py


# ---------------------------------------------
# EXECUTION
# ---------------------------------------------

FROM docker.io/library/python:3.12-slim

WORKDIR /home/jaime

USER root

RUN apt-get update && \
    apt-get install -y iputils-ping curl git wget procps 

COPY --from=compiler /home/src/jaime /usr/local/bin/jaime
RUN chmod +x /usr/local/bin/jaime

ENV HOME /home/jaime
ENV TZ=America/Argentina/Buenos_Aires

USER 1001

ENV PYTHON_HOST 0.0.0.0
ENV PYTHON_PORT 5000
ENV VERSION ${ARG_VERSION}
ENV JAIME_HOME_PATH /home/jaime/master/
ENV WORKINGDIR_PATH /home/jaime/workingdir/
ENV STORAGE_PATH /home/jaime/storage/

EXPOSE 5000

# CMD python3 -m gunicorn -b ${PYTHON_HOST}:${PYTHON_PORT} --workers=1 --threads=6 app:app
CMD jaime
