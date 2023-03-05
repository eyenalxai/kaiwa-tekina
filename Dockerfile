FROM python:slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1

RUN pip install pdm

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml
COPY ./pdm.lock /code/pdm.lock
RUN pdm install

COPY ./app /code/app
COPY main.py /code/main.py

ENV ADMIN_USER_IDS ${ADMIN_USER_IDS}
ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
ENV OPENAI_TOKEN ${OPENAI_TOKEN}
ENV FERNET_KEY ${FERNET_KEY}
ENV POLL_TYPE ${POLL_TYPE}
ENV DOMAIN ${DOMAIN}
ENV PORT ${PORT}

ARG EXPOSE_PORT=${PORT}
EXPOSE ${EXPOSE_PORT}

CMD ["pdm", "run", "start"]