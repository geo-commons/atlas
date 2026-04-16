# Atlas lokaal installeren

Zorg dat [Docker](https://www.docker.com/) op de lokale machine geïnstalleerd is.

Download Atlas van [GitLab](https://gitlab.com/purmerend/atlas) en pak het bestand uit op de computer.
Start Atlas met het volgende commando binnen de locatie waar de software is uitgepakt:

```bash
docker-compose up
```

Ga naar [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

De standaard instellingen zijn geschikt om Atlas mee te testen maar zijn niet geschikt voor een productieomgeving. Atlas kan geconfigureerd worden met de volgende settings:

- DEBUG: [Django](https://https://www.djangoproject.com/) [debug mode](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DEBUG). (standaard: False)
- SECRET_KEY: Django [secret key](https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-SECRET_KEY). Vervang door een gegenereerd wachtwoord in een productieomgeving. (standaard: changemetosomethingsecret)
- ALLOWED_HOSTS: Django [allowed hosts](https://docs.djangoproject.com/en/3.0/ref/settings/#allowed-hosts) setting. Een komma-gescheiden lijst van hosts waar de applicatie mag draaien. (standaard: localhost,127.0.0.1,[::1])
- ADMIN_IPS: Een komma-gescheiden lijst van hosts die toegang hebben tot de admin.
- INTERNAL_IPS: Een komma-gescheiden lijst van IP adressen die als intern gezien worden.
- DB_HOST: De host van de [Postgres](https://https://www.postgresql.org/) database. (standaard: postgres)
- DB_USER: De gebruikersnaam binnen de Postgres database. (standaard: atlas)
- DB_PASSWORD: Het wachtwoord van de Postgres database. Vervang door een gegenereerd wachtwoord in een productieomgeving. (standaard: atlas)
- DB_NAME: De databasenaam van de Postgres database. (standaard: atlas)
- SMARTSTREET_USER: De gebruikersnaam van de [Cyclomedia](https://www.cyclomedia.com/) Smartstreet API (voor gebruik binnen het interne netwerk).
- SMARTSTREET_PASSWORD: Het wachtwoord van de Cyclomedia Smartstreet API (voor gebruik binnen het interne netwerk).
- SMARTSTREET_API_KEY: De API key van de Cyclomedia Smartstreet API (voor gebruik binnen het interne netwerk).
- GOOGLE_MAPS_API_KEY: De [API key](https://developers.google.com/maps/documentation/javascript/get-api-key) voor Google Maps (voor extern gebruik).
- SENTRY_DSN: De [Sentry](https://sentry.io/) DSN om app statisitieken te verzamelen. (optioneel)

## Installeer een evaluatie-omgeving op Linux of MacOS

Zorg ervoor dat de volgende benodigdheden geïnstalleerd zijn:

- [Python 3](https://www.python.org)
- [Docker](https://www.docker.com)
- [pnpm](https://pnpm.io/) (installeer via `corepack enable`)

Atlas werkt met elke WMS, WFS en WMTS server als bron voor geo-ruimtelijke data. Datalab Purmerend gebruikt [Geoserver](https://github.com/geoserver/geoserver) om geo-ruimtelijke data te publiceren. Geoserver is slechts een mogelijke keus en is daarom niet als verplicht genoemd in een ontwikkelomgeving.

Geoserver is een open source software server, geschreven in Java, waarmee gebruikers georuimtelijke data kunnen bewerken en delen. Geoserver is speciaal gemaakt om de samenwerking tussen verschillende softwarecomponenten te vergemakkelijken. Het kan data publiceren van elke ruimtelijke-databron die open standaarden gebruikt.
De standaard ontwikkelomgeving van Atlas gebruikt de Purmerend Datalab Geoserver. Echter, wanneer je je eigen georuimtelijke data wilt publiceren (en dat wil je), dan moet uiteraard een aparte Geoserver opgezet worden.
Over het installeren en configureren van Geoserver is veel goede [documentatie](https://docs.geoserver.org/stable/en/user/) te vinden op internet.

Maak eerst een "virtual environment" aan voor Atlas:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Activeer een Postgres database server:

```bash
docker-compose up -d postgres
```

Voer de "database migrations" uit:

```bash
python3 manage.py migrate
```

en activeer de ontwikkelomgeving:

```bash
python3 manage.py runserver
```

Installeer nu de Node.js-afhankelijkheden:

```bash
cd ui/
pnpm install
```

en start een watch server:

```bash
pnpm run serve
```

Ga naar: [http://localhost:8000/atlas/](http://localhost:8000/atlas/).

## Laad demo data

Laad op de volgende manier demo data via de "backend":

```bash
python3 manage.py loaddata data/demo.json
```

Deze datadump bevat verschillende voorbeeldcategorieën en kaartlagen. Het maakt ook een superadmin gebruiker aan met de volgende eigenschappen:

- Gebruikersnaam: admin
- Wachtwoord: password

## Laad eigen data in Atlas

Om eigen data binnen Atlas als kaartlaag beschikbaar te maken moet deze data eerst in de Postgis database [geïmporteerd](https://postgis.net/workshops/postgis-intro/loading_data.html) worden. Daarna moet de data binnen [Geoserver](https://docs.geoserver.org/stable/en/user/) als laag bekend gemaakt worden waarna deze binnen Atlas geconfigureerd wordt. De configuratie binnen Atlas wordt behandeld in het Admin hoofdstuk.
Houd er rekening mee dat de geo-componend binnen de Postgis tabel voor Atlas altijd de veldnaam 'geom' moet hebben. Bij een andere veldnaam zal Atlas geen selecties kunnen doen op de data.

## Maak een superuser aan

Maak op de volgende wijze een supergebruiker aan:

```bash
python3 manage.py createsuperuser
```

Na het uitvoeren van de instructies kun je inloggen in de "backend" via: [http://localhost:8000/atlas/admin/](http://localhost:8000/atlas/admin/).

## Maak een hoofdkaart aan

Maak op de volgende wijze een hoofdkaart aan:

```bash
python3 manage.py ensure_main_map
```

Na het uitvoeren van dit commando is er een hoofdkaart in Atlas.
