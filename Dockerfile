FROM python:3.9.1-slim

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONBREAKPOINT=ipdb.set_trace

RUN apt update && apt install -y \
    gettext \
    libssl-dev \
    libffi-dev \
    make \
    gcc \
    git \
    libc-dev \
    musl-dev;

ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app
COPY poetry.lock* pyproject.toml /app/

ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root --no-interaction --no-ansi; else poetry install --no-root --no-dev --no-interaction --no-ansi; fi"

COPY src/ /app/src
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-interaction --no-ansi; else poetry install --no-dev --no-interaction --no-ansi; fi"

# COPY pytest.ini mypy.ini .flake8 /app/
ENV PYTHONPATH=/app/src
