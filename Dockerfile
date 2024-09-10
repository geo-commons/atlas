# UI
FROM node:20.11.1-alpine AS ui-build
WORKDIR /app/ui

COPY ui/package.json \
    ui/package-lock.json \
    /app/ui/
RUN npm install

COPY ui /app/ui
RUN npm run build

# API
FROM python:3.12-slim AS api-build
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential libgdal-dev

RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip

COPY requirements.txt /app
RUN /app/venv/bin/pip3 install -r requirements.txt

# Docs & Admin Docs
FROM python:3.12-slim as docs-build
WORKDIR /app/docs

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential libgdal-dev

RUN python -m venv /app/venv && /app/venv/bin/pip install --upgrade pip mkdocs

COPY requirements.txt /app/docs
RUN /app/venv/bin/pip3 install -r requirements.txt

COPY docs/user /app/docs/user
COPY docs/admin /app/docs/admin
COPY docs/user/mkdocs.yml /app/docs/user/mkdocs.yml
COPY docs/admin/mkdocs.yml /app/docs/admin/mkdocs.yml

RUN cd  /app/docs/user && /app/venv/bin/mkdocs build && cd /app/docs/admin && /app/venv/bin/mkdocs build

# Final container
FROM python:3.12-slim
WORKDIR /app

ARG ATLAS_VERSION=unknown

RUN apt-get update && apt-get install --no-install-recommends -y \
    mime-support \
    libxml2 \
    libgdal32 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN sed -i "s/unknown/${ATLAS_VERSION}/g" /app/atlas/__init__.py

COPY --from=api-build /app/venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"

COPY --from=ui-build /app/homepage/static/dist /app/homepage/static/dist
COPY --from=docs-build /app/docs/user/site /app/docs/user/site
COPY --from=docs-build /app/docs/admin/site /app/docs/admin/site

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /app/static /app/media && chown www-data:www-data /app/static /app/media /app/docs/user/site /app/docs/admin/site

ENV PYTHONUNBUFFERED 1
ENV ATLAS_ENVIRONMENT production

EXPOSE 8000
CMD ["/start.sh"]
USER www-data
