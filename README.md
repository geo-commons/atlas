# Atlas

[![Tests](https://github.com/geo-commons/atlas/actions/workflows/test.yml/badge.svg)](https://github.com/geo-commons/atlas/actions/workflows/test.yml)

Atlas is a geo portal that provides a user-friendly interface for layers on a WMS, WFS, WMTS and vector tiles (MVT)
server. Atlas is developed by [Datalab Purmerend](https://datalab.purmerend.nl/), part of Gemeente Purmerend,
and [Delta10](https://www.delta10.nl).

<img src="https://gitlab.com/purmerend/atlas/uploads/e549ad00397d4f0f593f703ee12ceb9b/image.png" alt="Screenshot of Atlas" width="500"/>

## Run Atlas locally

(For setting up a development environment, refer to the instructions below.)

Make sure you installed [Docker](https://www.docker.com/) on your local machine.

Download Atlas from [GitLab](https://gitlab.com/purmerend/atlas) and unpack the downloaded file on your computer.
Start Atlas by running the following command in the root of the repository:

```bash
docker compose up
```

If not existing yet, the above will also initialize a persistent Docker volume `atlas_postgres-data`, along with an
empty database. To import some test data:

```bash
docker compose exec atlas python3 manage.py loaddata data/demo.json
```

Browse to [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

### Load demo data

You can easily load demo data into the local backend with:

```bash
docker compose exec atlas python3 manage.py loaddata data/demo.json
```

This dump contains a demo user with the following credentials:

- Username: admin@example.com
- Password: password

### Updating frontend enums

If you make changes to the **metadataset option fields** in the Django models (e.g. `TextChoices` like topic categories,
roles, update methods), run:

```bash
pnpm run generate-metadata-types
```

This regenerates the frontend TypeScript enums and options so they stay in sync with the backend.

## Set up a development environment on Linux or macOS

Make sure you installed the following requirements:

- [uv](https://docs.astral.sh/uv/) (the Python package manager, which will automatically install Python if required)
- [Docker](https://www.docker.com)
- [Node.js](https://nodejs.org/) (version 22, other versions may work)
- [pnpm](https://pnpm.io/) (the Node.js package manager)
  - To install `pnpm`, we suggest using `corepack enable`, so that the correct version is 
    automatically installed according to `package.json`.

Apart from these requirements, Atlas works with the following services, which we suggest running
using Docker Compose:

- PostgreSQL
- [Geoserver](https://github.com/geoserver/geoserver) for serving geospatial data
- [filter-proxy](https://github.com/delta10/filter-proxy) to proxy requests to external APIs that need authorization (see below)
- The [Dex](https://dexidp.io) identity provider for user authentication

Apart from PostgreSQL, these are no hard dependencies, because Atlas can work with alternatives for these services. Atlas
can work with any WMS, WFS and WMTS server as a source of geospatial data. However, this setup
is common across Atlas installations and our demo data assumes that these services are running.

GeoServer is an open source software server written in Java that allows users to share and edit geospatial data.
Designed for interoperability, it publishes data from any major spatial data source using open standards.
The default development environment of Atlas uses the Purmerend Datalab Geoserver. However, if you want to present you
own geospatial data (and you do), you will need to run you own Geoserver.
There is a lot of very good [documentation](https://docs.geoserver.org/stable/en/user/) about Geoserver on the Internet.

We use the `uv` package manager in this project. Instead of activating a virtual environment
and installing the requirements, run `manage.py` with `uv run manage.py`.

Run a Postgres database server, filter-proxy, dex and GeoServer with:

```bash
docker compose up -d postgres dex filter-proxy geoserver
```

The above uses the same persistent volume `atlas_postgres-data` as used in [Run Atlas locally](#run-atlas-locally)
above. If it did not exist yet, run the database migrations with:

```bash
uv run manage.py migrate
```

And run the development server with:

```bash
uv run manage.py runserver
```

Now install the Node.js dependencies:

```bash
cd ui/
pnpm install
```

And start a watch server:

```bash
pnpm run dev
```

Run the mock api server:

- see [mock/README.md](mock/README.md)

Browse to [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

### Load demo data

You can easily load demo data into the local backend with:

```bash
uv run manage.py loaddata data/demo.json
```

This dump contains a demo user with the following credentials:

- Username: admin@example.com
- Password: password

## Filter proxy

The default setup runs a proxy in the background called [filter-proxy](https://github.com/delta10/filter-proxy). The
proxy can be used to authorize requests on OWS and REST services. When a request hits filter-proxy, it calls the
authorization endpoint of Atlas to see of the request is authorized. Atlas will look up the specific permissions of the
user and returns the decision. Based on the authorization, filter-proxy grants or denies access. Atlas also keeps an
audit log of successful authorization responses.

The setup using Docker Compose assumes that the host, which runs the Django application, can be
reached from the container running filter-proxy. Check firewall rules if this access appears to be blocked.
On Linux, you will have to add the following to the `filter-proxy` service in `docker-compose.yml`:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

## Settings

The default settings can be used for testing purposes, but are not suitable for production usage. Atlas can be
configured with the following settings:

-

DEBUG: [Django](https://https://www.djangoproject.com/) [debug mode](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DEBUG). (
default: False)

- SECRET_KEY: Django [secret key](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY). Replace
  with a generated password in production. (default: changemetosomethingsecret)
- ALLOWED_HOSTS: Django [allowed hosts](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) setting. A
  comma-seperated list of hosts that are allowed to serve the application. (default: localhost,127.0.0.1,[::1])
- ADMIN_IPS: A comma-seperated list of IP's that are allowed to access the admin.
- INTERNAL_IPS: A comma-seperated list of IP's that are seen as internal.
- DB_HOST: The host of the [Postgres](https://https://www.postgresql.org/) database. (default: postgres)
- DB_USER: The username of the Postgres database. (default: atlas)
- DB_PASSWORD: The password of the Postgres database. Replace with a generated password in production. (default: atlas)
- DB_NAME: The database name of the Postgres database. (default: atlas)
- SMARTSTREET_USER: The username of the [Cyclomedia](https://www.cyclomedia.com/) Smartstreet API (used internally).
- SMARTSTREET_PASSWORD: The password of the Cyclomedia Smartstreet API (used internally).
- SMARTSTREET_API_KEY: The API key of the Cyclomedia Smartstreet API (used internally).
- GOOGLE_MAPS_API_KEY: The [API key](https://developers.google.com/maps/documentation/javascript/get-api-key) for Google
  Maps (used externally).
- SENTRY_DSN: The [Sentry](https://sentry.io/) DSN to collect app statistics. (optional)

## Documentation (MkDocs)

The Atlas documentation is built using **MkDocs** and is split into two variants:

- **Admin documentation** – for configurators (_geo-beheerders_), covering the admin environment  
  Location: `docs/admin`

- **User documentation** – for end users of the Atlas application  
  Location: `docs/user`

### Run the documentation locally

**Admin docs**

```bash
cd docs/admin
uv run mkdocs serve
```

**User docs**

```bash
cd docs/user
mkdocs serve
```

## Frontend E2E tests (Playwright)

Run these from `ui/` after `pnpm install`. The app should be available at
`http://localhost:8000/atlas/` unless you set a different base URL.

```bash
cd ui
pnpm run test:e2e
```

Runs all Playwright E2E tests headlessly.

```bash
pnpm run test:e2e:ui
```

Opens Playwright's interactive test runner UI.

```bash
pnpm run test:e2e:record
```

Launches Playwright codegen to record a new test while you click through the app.

To use `test:e2e:ui` or `test:e2e:record`, install browser binaries once:

```bash
pnpx playwright install
```

Creating tests with codegen (Playwright record):
- Run `pnpm run test:e2e:record` and interact with the app to generate actions.
- Copy the generated test into your `ui/` Playwright test file(s), then run `pnpm run test:e2e`.
- For full usage details, see the Playwright codegen docs:

```
https://playwright.dev/docs/codegen
```

Optional environment variables:

- `PW_SKIP_WEBSERVER=1` to skip the Playwright webserver.
- `E2E_BASE_URL=http://localhost:8000/atlas/` for `test:e2e:record` to point codegen at a different URL.
