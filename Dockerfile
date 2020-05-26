FROM ubuntu:16.04
# FROM python:3.7-alpine

LABEL maintainer="Yoshiki Nakagawa <yoshiki.nakagawa10@gmail.com>"

ENV PYTHON_VERSION 3.7.3
ENV HOME /root
ENV PYTHON_ROOT $HOME/local/python-$PYTHON_VERSION
ENV PATH $PYTHON_ROOT/bin:$PATH
ENV PYENV_ROOT $HOME/.pyenv
RUN apt-get update && apt-get upgrade -y\
 && apt-get install -y \
    git \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
 && git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT \
 && $PYENV_ROOT/plugins/python-build/install.sh \
 && /usr/local/bin/python-build -v $PYTHON_VERSION $PYTHON_ROOT \
 && rm -rf $PYENV_ROOT

WORKDIR /opt/app

# export FLASK_APP=flask_app.py && export FLASK_RUN_PORT=80
ENV FLASK_APP=flaskr/flask_app.py
ENV FLASK_RUN_PORT=80
# ENV PRIMELY_ROOT=/opt/app

# RUN apk add --no-cache gcc musl-dev linux-headers

# RUN cd /opt && git clone https://github.com/yoshiki-o0/primely_docker_flask.git app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install primely package
COPY dist dist
RUN pip install dist/primely-0.0.1-py3-none-any.whl

COPY . .
RUN sh scripts/env.sh

CMD flask run --host=0.0.0.0
EXPOSE 80/tcp



