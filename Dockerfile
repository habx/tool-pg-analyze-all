FROM python:3.11.5-slim

ARG CREATED
ARG REVISION
ARG VERSION
ARG TITLE
ARG SOURCE
ARG AUTHORS
ARG GEMFURY_READ_TOKEN
ARG GEMFURY_ORGA
LABEL org.opencontainers.image.created=$CREATED \
        org.opencontainers.image.revision=$REVISION \
        org.opencontainers.image.title=$TITLE \
        org.opencontainers.image.source=$SOURCE \
        org.opencontainers.image.version=$VERSION \
        org.opencontainers.image.authors=$AUTHORS \
        org.opencontainers.image.vendor="Habx"

WORKDIR /app
COPY main.py Pipfile* build.json package.json /app/
RUN pip3 install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

ENTRYPOINT ["python3","/app/main.py"]
