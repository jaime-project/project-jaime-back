# COMPILER
# ---------------------------------------------
FROM python:3.9-slim as compiler

WORKDIR /home/src
COPY . .

RUN pip3 install compile --upgrade pip

RUN	python -m compile -b -f -o dist/ .


# EXECUTION
# ---------------------------------------------
FROM python:3.9-slim

WORKDIR /home/src

RUN apt-get update
RUN apt-get install iputils-ping curl git -y

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=80
ENV WORKINGDIR_PATH=/data/workingdir

ENV TZ America/Argentina/Buenos_Aires
ENV PYTHONPATH "${PYTHONPATH}:/home/src"

CMD gunicorn \
    -b ${PYTHON_HOST}:${PYTHON_PORT} \
    --workers=1 \
    --threads=6 \
    app:app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt --upgrade pip
RUN rm -fr requirements.txt

COPY --from=compiler /home/src/dist/ ./
