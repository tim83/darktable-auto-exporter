FROM debian:bookworm-20250224

RUN apt-get update
RUN apt-get install darktable

ENTRYPOINT ["darktable-cli"]