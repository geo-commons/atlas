# UI
FROM node:24.20.0-alpine AS ui-build
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
WORKDIR /app/ui

COPY ui/package.json \
    ui/pnpm-lock.yaml \
    ui/pnpm-workspace.yaml \
    /app/ui/
RUN corepack enable
RUN pnpm install --frozen-lockfile

COPY ui /app/ui
RUN pnpm run build

# API

# Following the example of uv in Docker from
# https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile

FROM python:3.13-slim AS api-build
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential libgdal-dev

RUN pip install uv

COPY pyproject.toml uv.lock /app/

# Install Python to a place that we can copy in the final container
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv sync --frozen --no-dev --group prod --link-mode copy

# Docs & Admin Docs
FROM python:3.13-slim AS docs-build
WORKDIR /app/docs

COPY --from=api-build /app/.venv /app/.venv
COPY --from=api-build /python /python
ENV PATH="/app/.venv/bin:${PATH}"

COPY docs/user /app/docs/user
COPY docs/admin /app/docs/admin
COPY docs/user/mkdocs.yml /app/docs/user/mkdocs.yml
COPY docs/admin/mkdocs.yml /app/docs/admin/mkdocs.yml

RUN cd  /app/docs/user && python -m mkdocs build && cd /app/docs/admin && python -m mkdocs build

# Final container
FROM python:3.13-slim
WORKDIR /app

ARG ATLAS_VERSION=unknown

RUN apt-get update && apt-get install --no-install-recommends -y \
    media-types \
    libxml2 \
    libgdal36 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN sed -i "s/unknown/${ATLAS_VERSION}/g" /app/atlas/__init__.py

COPY --from=api-build /app/.venv /app/.venv
COPY --from=api-build /python /python
ENV PATH="/app/.venv/bin:${PATH}"

COPY --from=ui-build /app/homepage/static/dist /app/homepage/static/dist
COPY --from=docs-build /app/docs/user/site /app/docs/user/site
COPY --from=docs-build /app/docs/admin/site /app/docs/admin/site

COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

RUN mkdir -p /app/static /app/media && chown www-data:www-data /app/static /app/media /app/docs/user/site /app/docs/admin/site

ENV PYTHONUNBUFFERED=1
ENV USE_SAFE_SETTINGS=1
ENV ENVIRONMENT=production

EXPOSE 8000
CMD ["/start.sh"]
USER www-data
