FROM python:3.8-slim AS build
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip

COPY requirements.txt /app
RUN /app/venv/bin/pip3 install -r requirements.txt

FROM python:3.8-slim
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    mime-support \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

COPY --from=build /app/venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /app/static && chown www-data:www-data /app/static

ENV PYTHONUNBUFFERED 1
ENV ATLAS_ENVIRONMENT production

EXPOSE 8000
CMD ["/start.sh"]
USER www-data
