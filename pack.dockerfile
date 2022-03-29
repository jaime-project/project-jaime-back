# COMPILER
# ---------------------------------------------
FROM python:3.9 as compiler

WORKDIR /home/src
COPY . .

RUN pip install -r requirements.txt --upgrade pip
RUN pyinstaller --add-binary logic:logic -n jaime --onefile app.py

# EXECUTION
# ---------------------------------------------
FROM ubuntu:22.04

WORKDIR /root

ARG ARG_VERSION=local

ENV VERSION=${ARG_VERSION}
ENV TZ America/Argentina/Buenos_Aires
ENV PYTHON_HOST=0.0.0.0
ENV PYTHON_PORT=80
ENV WORKINGDIR_PATH=/data/workingdir

COPY --from=compiler /home/src/dist/jaime ./
COPY *.json ./
COPY variables.yaml ./

CMD ./jaime
