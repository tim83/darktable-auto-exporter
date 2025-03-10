FROM debian:bookworm-20250224

RUN apt-get update
RUN apt-get install -y darktable pipx
RUN pipx install poetry

COPY . /app
WORKDIR /app

RUN poetry install --without=dev --no-interaction

ENTRYPOINT ["poetry run darktable-auto-exporter"]