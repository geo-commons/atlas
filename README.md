# Atlas 

Atlas is a geo portal that provides a user-friendly interface for layers on a WMS, WFS, WMTS and vector tiles (MVT) server. Atlas is developed by [Datalab Purmerend](https://datalab.purmerend.nl/), part of Gemeente Purmerend and [Delta10](https://www.delta10.nl).

<img src="https://gitlab.com/purmerend/atlas/uploads/e549ad00397d4f0f593f703ee12ceb9b/image.png" alt="Screenshot of Atlas" width="500"/>

## Run Atlas locally

Make sure you installed [Docker](https://www.docker.com/) on your local machine.

Download Atlas from [GitLab](https://gitlab.com/purmerend/atlas) and unpack the downloaded file on your computer.
Start Atlas by running the following command in the root of the repository:

```bash
docker-compose up
```

Browse to [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

The default settings can be used for testing purposes, but are not suitable for production usage.

Adjust the `.env` file to configure the application and create a secure production setup. The file contains the following settings:

- DEBUG: [Django](https://https://www.djangoproject.com/) [debug mode](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DEBUG). (default: False)
- SECRET_KEY: Django [secret key](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY). Replace with a generated password in production. (default: changemetosomethingsecret)
- ALLOWED_HOSTS: Django [allowed hosts](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) setting. A comma-seperated list of hosts that are allowed to serve the application. (default: localhost,127.0.0.1,[::1])
- CTRIX_IPS: A comma-seperated list of IP's that are internal in the application.
- DB_HOST: The host of the [Postgres](https://https://www.postgresql.org/) database. (default: postgres)
- DB_USER: The username of the Postgres database. (default: atlas)
- DB_PASSWORD: The password of the Postgres database. Replace with a generated password in production. (default: atlas)
- DB_NAME: The database name of the Postgres database. (default: atlas)
- WFS_URL: The URL of the external WFS server (e.g. [Geoserver](https://github.com/geoserver/geoserver)).
- WFS_URL_CTRIX: The URL if the internal WFS server (e.g. Geoserver).
- SMARTSTREET_USER: The username of the [Cyclomedia](https://www.cyclomedia.com/) Smartstreet API (used internally).
- SMARTSTREET_PASSWORD: The password of the Cyclomedia Smartstreet API (used internally).
- SMARTSTREET_API_KEY: The API key of the Cyclomedia Smartstreet API (used internally).
- GOOGLE_MAPS_API_KEY: The [API key](https://developers.google.com/maps/documentation/javascript/get-api-key) for Google Maps (used externally).
- SENTRY_DSN: The [Sentry](https://sentry.io/) DSN to collect app statistics. (optional)

## Setup a development environment on Linux or MacOS

Make sure you installed the following requirements:

- [Python 3](https://www.python.org)
- [Docker](https://www.docker.com)

Atlas can work with any WMS, WFS and WMTS server as a source of geospatial data. Datalab Purmerend relies on [Geoserver](https://github.com/geoserver/geoserver) for viewing geospatial data. Since Geoserver is one possible choice, it is not listed as a requirement to set up a development environment.

GeoServer is an open source software server written in Java that allows users to share and edit geospatial data. Designed for interoperability, it publishes data from any major spatial data source using open standards.
The default development environment of Atlas uses the Purmerend Datalab Geoserver. However, if you want to present you own geospatial data (and you do), you will need to run you own Geoserver.
There is a lot of very good [documentation](https://docs.geoserver.org/stable/en/user/) about Geoserver on the Internet.

First setup a new virtual environment for Atlas with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Run a Postgres database server with:

```bash
docker-compose up -d postgres
```

Now run the database migrations with:

```bash
python3 manage.py migrate
```

And run the development server with:

```bash
python3 manage.py runserver
```

Now install the npm dependencies:

```bash
cd ui/
npm install
```

And start a watch server:

```bash
npm run serve
```

Browse to [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

### Load demo data

You can easily load demo data into the local backend with:

```bash
python3 manage.py loaddata data/demo.json
```

This dump contains some example categories and layers and also creates a superadmin user with the following credentials:

- Username: admin
- Password: password

### Create a superuser

To create a new superuser use the following command:

```bash
python3 manage.py createsuperuser
```

Follow the steps. You can now login to [http://localhost:8000/atlas/admin/](http://localhost:8000/atlas/admin/).
