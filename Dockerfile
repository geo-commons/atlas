# UI
FROM node:19.7.0-alpine AS ui-build
WORKDIR /app/ui

COPY ui/package.json \
    ui/package-lock.json \
    /app/ui/
RUN npm install

COPY ui /app/ui
RUN npm run build

# API
FROM python:3.11-slim AS api-build
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential

RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip

COPY requirements.txt /app
RUN /app/venv/bin/pip3 install -r requirements.txt

# Final container
FROM python:3.11-slim
WORKDIR /app

ARG ATLAS_VERSION=unknown

RUN apt-get update && apt-get install --no-install-recommends -y \
    mime-support \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN sed -i "s/unknown/${ATLAS_VERSION}/g" /app/atlas/__init__.py

COPY --from=api-build /app/venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"

COPY --from=ui-build /app/homepage/static/dist /app/homepage/static/dist
COPY --from=ui-build /app/ui/webpack-stats.json /app/ui/webpack-stats.json

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /app/static /app/media && chown www-data:www-data /app/static /app/media

ENV PYTHONUNBUFFERED 1
ENV ATLAS_ENVIRONMENT production

EXPOSE 8000
CMD ["/start.sh"]
USER www-data
