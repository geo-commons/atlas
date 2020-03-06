# Atlas
Atlas is a geo portal that provides a user-friendly interface for layers on a WFS server. Atlas is developed by [Datalab Purmerend](https://datalab.purmerend.nl/), part of Gemeente Purmerend.

<img src="https://gitlab.com/purmerend/atlas/uploads/3c5ed4d1d65ab0ac67e958b9264ab149/image.png" alt="Screenshot of Atlas" width="500"/>

## Run Atlas locally
Make sure you installed [Docker](https://www.docker.com/) on your local machine.

Start Atlas by running the following command in the root of the repository:

```bash
docker-compose up
```

Browse to [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

The default settings can be used for testing purposes, but are not suitable for production usage.

Adjust the `.env` file to configure the application and create a secure production setup. The file contains the following settings:

- DEBUG: Django [debug mode](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DEBUG). (default: False)
- SECRET_KEY: Django [secret key](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY). Replace with a generated password in production. (default: changemetosomethingsecret)
- ALLOWED_HOSTS: Django [allowed hosts](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) setting. A comma-seperated list of hosts that are allowed to serve the application. (default: localhost,127.0.0.1,[::1])
- CTRIX_IPS: A comma-seperated list of IP's that are internal in the application.
- DB_HOST: The host of the Postgres database. (default: postgres)
- DB_USER: The username of the Postgres database. (default: atlas)
- DB_PASSWORD: The password of the Postgres database. Replace with a generated password in production. (default: atlas)
- DB_NAME: The database name of the Postgres database. (default: atlas)
- WFS_URL: The URL of the external WFS server (e.g. Geoserver).
- WFS_URL_CTRIX: The URL if the internal WFS server (e.g. Geoserver).
- SMARTSTREET_USER: The username of the Cyclomedia Smartstreet API (used internally).
- SMARTSTREET_PASSWORD: The password of the Cyclomedia Smartstreet API (used internally).
- SMARTSTREET_API_KEY: The API key of the Cyclomedia Smartstreet API (used internally).
- GOOGLE_MAPS_API_KEY: THe API key for Google Maps (used externally).

## Setup a development environment
Make sure you installed the following requirements:

- [Python 3](https://www.python.org)
- [Docker](https://www.docker.com)

First setup a new virtual environment for Atlas with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

Browse to [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

### Create a superuser
To create a new superuser use the following command:

```bash
python3 manage.py createsuperuser
```

Follow the steps. You can now login to [http://localhost:8000/atlas/admin/](http://localhost:8000/atlas/admin/).