FROM registry.opensuse.org/opensuse/tumbleweed:20250321

RUN zypper refresh
RUN zypper install -y darktable python3-poetry

COPY . /app
WORKDIR /app

RUN poetry install --without=dev --no-interaction

ENTRYPOINT ["poetry", "run" ,"darktable-auto-exporter"]