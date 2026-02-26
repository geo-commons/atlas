# Metadata

Metadata in Atlas beschrijft de eigenschappen en kenmerken van datasets. Atlas ondersteunt uitgebreide metadata conform
de standaard ISO 19115. Zie
het [overzicht van metadata-elementen volgens het Nederlandse profiel op ISO 19115](https://docs.geostandaarden.nl/md/mdprofiel-iso19115/#metadata-elementen-overzicht)
voor een volledige beschrijving van de velden. Deze handleiding beschrijft hoe je metadata beheert binnen de Atlas Admin
Module.

## Overzicht

Atlas gebruikt **Metadatasets** voor het beheren van metadata. Metadatasets bevatten uitgebreide informatie over
datasets zoals herkomst, kwaliteit, contact informatie en gebruiksvoorwaarden.

Metadatasets kunnen worden gekoppeld aan meerdere kaartlagen. Alle metadata wordt centraal beheerd via metadatasets.

## Metadatasets beheren

### Metadatasets lijst

Ga naar **Metadatasets** in het hoofdmenu van de admin module om een overzicht te krijgen van alle metadatasets.

De lijst toont:

- **Titel**: De titel van de metadataset
- **Onderwerp**: Het hoofdonderwerp van de dataset
- **Status**: De huidige status van de dataset
- **Toon op portal**: Of de dataset zichtbaar is in het publieke dataportaal

### Nieuwe metadataset aanmaken

1. Klik op **Toevoegen** in de metadatasets lijst
2. Vul de verplichte velden in:
   - **Titel**: Beschrijvende naam van de dataset
   - **Beschrijving**: Beschrijving voor intern gebruik

## Metadataset velden

### Algemene informatie

**Naam** _(Publiek)_
De naam van de metadataset. Dit is de naam die wordt weergegeven in de interface. Gebruik een duidelijke, beschrijvende
naam.

**Kort kenmerk** _(Publiek)_
Een uniek kort kenmerk voor de metadataset in Atlas. Gebruik alleen kleine letters, cijfers en afbreekstreepjes. Dit
wordt gebruikt in URLs en koppelingen. Maximaal 255 karakters.

**Beschrijving** _(Intern)_
Beschrijving voor intern gebruik. [Markdown](markdown.md) opmaak is toegestaan.

**Toelichting dataset** _(Publiek)_
Een beschrijving van de inhoud van de dataset. Geef in deze samenvatting publieksvriendelijke informatie over de inhoud
van de dataset. Deze is minimaal drie zinnen en maximaal één alinea lang (2000 karakters).

**Onderwerp** _(Publiek)_
Het belangrijkste onderwerp van de dataset uit een voorgedefinieerde lijst:

- Landbouw en Veeteelt
- Biodiversiteit en Ecologie
- Grenzen en Administratie
- Klimaat en Meteorologie
- Economie en Werkgelegenheid
- Hoogte en Reliëf
- Milieu en Natuurbescherming
- Geowetenschappen
- Gezondheid en Veiligheid
- Basiskaarten en Beeldmateriaal
- Defensie en Militaire Zaken
- Binnenwateren
- Locatie en Adressering
- Oceanen en Kustgebieden
- Ruimtelijke Ordening en Kadaster
- Maatschappij en Cultuur
- Bouwwerken en Infrastructuur
- Transport en Vervoer
- Nutsvoorzieningen en Communicatie

**Trefwoorden** _(Publiek)_
In het algemeen gebruikte woorden of geformaliseerde zinnen om een dataset of datasetserie te beschrijven. Voeg één
trefwoord per regel toe.

**Doel van de vervaardiging** _(Publiek)_
De reden waarom de dataset is gemaakt.

### Bron

**Oorspronkelijke bron** _(Publiek)_
Algemene beschrijving herkomst. Dit is de bron waar de dataset vandaan komt, dat kan een URL zijn of een beschrijving
van de bron.

**Bronlocatie** _(Intern)_
Bijvoorbeeld Objectstore (COG), S3, etc.

**Naam contactpersoon aanspreekpunt** _(Intern)_
De naam van het interne aanspreekpunt van de bron.

**E-mailadres aanspreekpunt** _(Intern)_
Het e-mailadres van het interne aanspreekpunt van de bron.

**Verantwoordelijke organisatie** _(Publiek)_
De organisatie van de verantwoordelijke van de bron, bijvoorbeeld de gemeente, provincie, Nederlandse organisatie voor
toegepast-natuurwetenschappelijk onderzoek (TNO), etc.

**Naam contactpersoon aanspreekpunt** _(Publiek)_
De naam van de verantwoordelijke contactpersoon van de bron.

**E-mailadres verantwoordelijke** _(Publiek)_
Het e-mailadres van de verantwoordelijke organisatie van de bron.

**Rol verantwoordelijke** _(Publiek)_
De rol van de verantwoordelijke over de bron:

- Data verstrekker
- Beheerder
- Eigenaar
- Gebruiker
- Distributeur
- Maker
- Contactpunt
- Onderzoeksleider
- Bewerker
- Uitgever
- Auteur

### Status

**Updatemethode** _(Intern)_
De methode waarmee de dataset wordt bijgewerkt:

- Manueel
- Automatisch

**Updatefrequentie** _(Publiek)_
De frequentie waarmee de dataset wordt bijgewerkt. Bijvoorbeeld: dagelijks, wekelijks, maandelijks, jaarlijks.

**Laatst bijgewerkt** _(Publiek)_
De datum waarop de dataset voor het laatst is bijgewerkt.

**Status**
De huidige status van de dataset:

- Gepubliceerd
- In ontwikkeling
- Gearchiveerd

**Toon in dataportaal voor niet-ingelogde gebruikers**
Schakel in om de metadataset in het dataportaal te tonen voor niet-ingelogde gebruikers. Ingelogde gebruikers zien
gepubliceerde metadatasets altijd.

### Beperkingen

**Juridische toegangsrestricties** _(Publiek)_
Juridische toegangsrestricties die van toepassing zijn op de dataset:

- Licentie - Formele toestemming om iets te doen met de data
- Intellectuele eigendomsrechten - Recht op een financieel voordeel van - en controle hebben op de distributie van een
  niet tastbaar eigendom dat het resultaat is van creativiteit.
- Beperkt - Verbod op distributie en gebruik
- Overige beperkingen - Restrictie niet opgenomen in lijst

**Overige beperkingen** _(Publiek)_
Selecteer een optie wanneer je bij juridische toegangsrestricties 'Overige beperkingen' hebt gekozen:

- Open data (publiek)
- Open data (CC0)
- Open data (CC-BY)
- Open data (CC-BY-SA)
- Open data (CC-BY-NC)
- Gebruiksvoorwaarden (CC-by-nc-sa)
- Gebruiksvoorwaarden (CC-by-nd)
- Gebruiksvoorwaarden (CC-by-nc-nd)
- Gebruiksvoorwaarden Geogedeeld

**Gebruiksbeperkingen**
In dit veld geef je aan waarvoor de dataset niet mag of kan worden gebruikt. Bijvoorbeeld: Niet gebruiken voor
navigatie.

### Verantwoordelijke metadata

**E-mailadres aanspreekpunt** _(Intern)_
Het e-mailadres van het interne aanspreekpunt van de verantwoordelijke van de metadata.

**Organisatie** _(Publiek)_
De naam van de organisatie verantwoordelijk voor de metadata. Gebruik de volledig uitgeschreven naam van de
verantwoordelijke organisatie. Bijvoorbeeld: Gemeente Purmerend.

**E-mailadres verantwoordelijke** _(Publiek)_
Het e-mailadres van de organisatie verantwoordelijk voor de metadata. Gebruik bij voorkeur een functioneel e-mailadres.

**Rol verantwoordelijke** _(Publiek)_
De rol van de verantwoordelijke over de metadata:

- Data verstrekker
- Beheerder
- Eigenaar
- Gebruiker
- Distributeur
- Maker
- Contactpunt
- Onderzoeksleider
- Bewerker
- Uitgever
- Auteur

## Metadata koppelen aan kaartlagen

### Via kaartlaag bewerken

1. Ga naar **Kaartlagen** in het hoofdmenu
2. Selecteer de kaartlaag die je wilt bewerken
3. In het **Algemene gegevens** gedeelte vind je het **Metadata** veld
4. Selecteer de gewenste metadataset uit de dropdown
5. Sla de wijzigingen op

!!! info "Publicatie vereiste"
Een kaartlaag kan alleen worden gepubliceerd als er een metadataset aan is gekoppeld. Dit is nodig zodat gebruikers
altijd toegang hebben tot de juiste beschrijvende informatie (metadata) over de kaartlaag. Zonder gekoppelde metadataset
ontbreekt deze informatie en voldoet de publicatie niet aan de kwaliteits- en transparantie-eisen.

### Gekoppelde kaartlagen bekijken

Bij het bewerken van een metadataset zie je onderaan een lijst van alle kaartlagen die aan deze metadataset zijn
gekoppeld.

## Metadata in Atlas frontend

### Metadata bekijken

Gebruikers kunnen metadata bekijken door:

1. Een kaartlaag te selecteren in het **Zichtbare lagen** menu
2. Op het ⓘ (informatie) icoon te klikken
3. De metadata wordt getoond in een popup

### Metadata pagina

Elke kaartlaag heeft een eigen metadata pagina bereikbaar via:

```
https://jouw-atlas-url/metadata/kort-kenmerk-kaartlaag
```

Het korte kenmerk van de kaartlaag wordt gebruikt voor deze URL.

## Import en export

### Metadatasets exporteren

1. Ga naar de **Metadatasets** lijst
2. Selecteer de metadatasets die je wilt exporteren
3. Kies **Exporteer geselecteerde metadatasets** uit het acties menu
4. Kies het gewenste formaat (CSV, Excel, JSON)

### Metadatasets importeren

1. Klik op **Importeren** in de metadatasets lijst
2. Upload een bestand met metadataset gegevens
3. Controleer de preview van te importeren gegevens
4. Bevestig de import

!!! warning "Import validatie"
Zorg ervoor dat korte kenmerken uniek zijn en verplichte velden zijn ingevuld bij het importeren van metadatasets.

## Best practices

### Naamgeving

- Gebruik duidelijke, beschrijvende namen voor metadatasets
- Korte kenmerken moeten logisch en herkenbaar zijn
- Vermijd spaties en speciale tekens in korte kenmerken

### Compleetheid

- Vul alle relevante velden in voor betere vindbaarheid
- Gebruik consistente terminologie binnen uw organisatie
- Houd contactgegevens actueel

### Onderhoud

- Controleer regelmatig of metadata nog actueel is
- Update "Laatst bijgewerkt" velden bij wijzigingen in de data
- Archiveer verouderde metadatasets

### Kwaliteit

- Schrijf publieksvriendelijke beschrijvingen
- Test metadata links regelmatig op geldigheid

## Integratie met externe systemen

### MBS (Metadata Beheersysteem)

Atlas is geïntegreerd met het Metadata Beheersysteem (MBS). Metadatasets worden automatisch gesynchroniseerd met MBS
voor publicatie in externe catalogi.

### API toegang

Metadata is toegankelijk en bewerkbaar via de Atlas API. Hiermee kun je niet alleen metadatasets opvragen, maar ook
metadata-velden zoals de "Laatst bijgewerkt" datum aanpassen. Dit is handig wanneer je wijzigingen in de dataset hebt
doorgevoerd en de metadata up-to-date wilt houden.

Voorbeelden van API-endpoints:

- **Lijst van metadatasets ophalen (GET):**

  ```
  GET /atlas/api/v1/metadatasets/
  ```

- **Details van een specifieke metadataset ophalen (GET):**

  ```
  GET /atlas/api/v1/metadatasets/<id>/
  ```

- **Een nieuwe metadataset aanmaken (POST):**

  ```
  POST /atlas/api/v1/metadatasets/
  Content-Type: application/json

  {
    "title": "Voorbeeld dataset",
    "slug": "voorbeeld-dataset",
    "abstract": "Korte publieksvriendelijke beschrijving...",
    ...
  }
  ```

- **Een metadataset bijwerken, bijvoorbeeld het veld "Laatst bijgewerkt" aanpassen (PATCH):**

  ```
  PATCH /atlas/api/v1/metadatasets/<id>/
  Content-Type: application/json

  {
    "last_updated": "2025-09-22"
  }
  ```

- **Een metadataset verwijderen (DELETE):**

  ```
  DELETE /atlas/api/v1/metadatasets/<id>/
  ```

**Voorbeeld: "Laatst bijgewerkt" aanpassen via de API**

Stel, je wilt het veld "Laatst bijgewerkt" van een metadataset met id 42 aanpassen naar 22 september 2025. Gebruik dan
het volgende verzoek:

```bash
curl -X PATCH "https://<jouw-atlas-url>/atlas/api/v1/metadatasets/42/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "last_updated": "2025-09-22"
  }'
```

Dit is vooral nuttig voor automatische processen die dagelijks data vernieuwen en de metadata willen bijwerken.
