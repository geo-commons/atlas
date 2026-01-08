In dit artikel wordt uitgelegd wat "Tabellen" zijn, wat je ermee kan en hoe je ze configureert.


## Wat zijn tabellen? 
Tabellen zijn raadpleegbaar via kaartlagen in de kaartviewer. Via een aan een kaartlaag gekoppelde tabel kan je een lijstweergave met resultaten vanuit een OWS / REST bron weergeven en door op een resultaat in de lijstweergave te drukken kan je een bijbehorende detailweergave bekijken. Tabellen kunnen geraadpleegd worden voor het tonen van (geo-)informatie vanuit diverse type (OWS en REST) bronnen waar niet altijd een geometrie aanhangt. 

Een bijkomende kracht van tabellen is dat je ze aan elkaar kan verbinden, waardoor je in de detailweergave van een tabel de lijstweergaves van andere tabellen kan tonen. Daarnaast is een tafel erg flexibel te configureren, waardoor je ze voor veel verschillende doeleinden kan inzetten.

### Voorbeeld
<img src="../images/kaartlaag-bag-standligplaatsen.png" alt="Kaartlaag BAG standligplaatsen met gekoppelde tabel" width="800"/>
In dit voorbeeld zie je een kaartlaag (BAG pand, stand- en ligplaats) waarbij de detailweergave van gebouw met Gebouw id 9180 openstaat. Onderaan zie je dat er aan deze kaartlaag een tabel is gekoppeld. Op basis van beschikbare informatie van het specifieke aangeklikte object op de BAG pand, stand- en ligplaats kaartlaag met Gebouw ID 9180 wordt een OWS verzoek gedaan naar een BAG Adressen kaartlaag en de resultaten worden weergegeven in de bijbehorende lijstweergave.

<img src="../images/tabel-detailweergave-adressen.png" alt="Detailweergave van een adres" width="800"/>
In de bovenstaande screenshot zie je de detailweergave van een adres uit de lijstweergave. Daarnaast zie je dat er een "subbuurten" tabel aan deze tabel is gekoppeld, waardoor op basis van de beschikbare informatie van het adres object de bijbehorende subbuurten voor dit adres worden opgehaald.

# Het configureren van tabellen
Het configureren van tabellen verloopt via de Atlas admin. In dit artikel wordt per veld uitgelegd wat ermee geconfigureerd kan worden en daarnaast wordt er een voorbeeld gegeven van een mogelijke configuratie voor een KvK tabel, die resultaten uit de KVK ZOEKEN api toont.

## Basisinformatie

| Veld | Uitleg | Validatie | Voorbeeld (KVK) |
|------|--------|-----------|-----------------|
| **Titel** | De titel van de tabel wordt zowel in de lijstweergave als in de detailweergave getoond. | Verplicht, maximaal 128 karakters | `Bedrijven`     |
| **Kort kenmerk** | De slug (korte identifier) van de tabel. Dit wordt gebruikt in URL's en interne verwijzingen. | Verplicht, maximaal 255 karakters | `bedrijven`     |

### Bronconfiguratie

| Veld | Uitleg | Validatie | Voorbeeld (KVK)                   |
|------|--------|-----------|-----------------------------------|
| **Bron** | De URL van de externe databron waarmee de tabel verbinding maakt. Dit kan een OWS (OGC Web Service) of REST API zijn. | Verplicht | `https://api.kvk.nl/test/api/v2/` |
| **Type bron** | Het type API dat wordt gebruikt voor het ophalen van gegevens. Keuze tussen REST of OWS. | Verplicht | `REST`                            |

### Veldconfiguratie

| Veld | Uitleg                                                                                                                                                                                                                                                                   | Validatie | Voorbeeld (KVK)                                                                                                                                                                                                                                                                                 |
|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Beschikbare velden** | Een lijst met velden uit het API-resultaat die je wilt gebruiken in je tabel. Je kunt objectnotatie gebruiken om geneste velden aan te spreken.<br><br>**Objectnotatie:**<br>• Genest object: `adres.binnenlandsAdres.type`<br>• Array element: `adres.adressen[0].type` | Optioneel | `kvkNummer`<br>`rsin`<br>`vestigingsnummer`<br>`type`<br>`naam`<br>`adres.binnenlandsAdres.type`<br>`adres.binnenlandsAdres.straatnaam`<br>`adres.binnenlandsAdres.huisnummer`<br>`adres.binnenlandsAdres.huisletter`<br>`adres.binnenlandsAdres.postcode`<br>`adres.binnenlandsAdres.plaats` |
| **Toon deze velden in de lijstweergave** | Bepaal welke velden zichtbaar zijn in het overzicht met meerdere resultaten. Indien dit veld niet is ingevuld worden alle velden getoond.                                                                                                                                | Optioneel | `kvkNummer`<br>`naam`<br>`adres.binnenlandsAdres.straatnaam`<br>`adres.binnenlandsAdres.huisnummer`<br>`adres.binnenlandsAdres.huisletter`                                                                                                                                                    |
| **Toon deze velden in de detailweergave** | Bepaal welke velden zichtbaar zijn wanneer een individueel item wordt bekeken. Indien dit veld niet is ingevuld worden alle velden getoond.                                                                                                                              | Optioneel | `kvkNummer`<br>`naam`<br>`adres.binnenlandsAdres.straatnaam`<br>`adres.binnenlandsAdres.huisnummer`<br>`adres.binnenlandsAdres.huisletter`                                                                                                                                                    |

## REST-specifieke configuratie
### REST API endpoints

| Veld | Uitleg | Validatie | Voorbeeld (KVK)                                                                     |
|------|--------|-----------|-------------------------------------------------------------------------------------|
| **Lijst endpoint** | Het API-endpoint voor het ophalen van meerdere resultaten. Je kunt dynamische waarden meegeven via template tags tussen dubbele accolades: `{{variabele}}` | Optioneel (verplicht bij REST bron) | `/zoeken?postcode={{postcode}}&huisnummer={{huisnummer}}&huisletter={{huisletter}}` |
| **Detail endpoint** | Het API-endpoint voor het ophalen van één specifiek resultaat. Ook hier kun je template tags gebruiken: `{{variabele}}` | Optioneel (verplicht bij REST bron) | `/zoeken?kvkNummer={{kvkNummer}}`                                                   |

### Response mapping

| Veld | Uitleg | Validatie | Voorbeeld (KVK) |
|------|--------|-----------|-----------------|
| **Veldnaam van lijst** | Het pad in de API-response waar de array met resultaten staat voor de lijstweergave. Gebruik objectnotatie voor geneste velden. | Optioneel | `resultaten`    |
| **Veldnaam van detailweergave** | Het pad in de API-response waar het individuele resultaat staat voor de detailweergave. Gebruik objectnotatie voor geneste velden. | Optioneel | `resultaten[0]` |

### Paginering

| Veld | Uitleg | Validatie | Voorbeeld (KVK)       |
|------|--------|-----------|-----------------------|
| **URL parameter voor pagina** | De naam van de URL-parameter waarmee je aangeeft welke pagina moet worden opgehaald. | Optioneel | `pagina`              |
| **URL parameter voor items per pagina** | De naam van de URL-parameter waarmee je aangeeft hoeveel resultaten per pagina moeten worden getoond. | Optioneel | `resultatenPerPagina` |
| **Veldnaam van totaal aantal items** | Het pad in de API-response waar het totale aantal beschikbare items staat. Dit wordt gebruikt voor paginering. Gebruik objectnotatie voor geneste velden. | Optioneel | `totaal`              |

### Foutafhandeling

| Veld | Uitleg | Validatie | Voorbeeld (KVK)        |
|------|--------|-----------|------------------------|
| **Veldnaam van foutmelding in lijstweergave** | Het pad in de API-response waar foutmeldingen staan bij mislukte verzoeken voor de lijstweergave. Gebruik objectnotatie voor geneste velden. | Optioneel | `fout[0].omschrijving` |
| **Veldnaam van foutmelding in detailweergave** | Het pad in de API-response waar foutmeldingen staan bij mislukte verzoeken voor de detailweergave. Gebruik objectnotatie voor geneste velden. | Optioneel | `fout[0].omschrijving` |

## OWS-specifieke configuratie
### CQL filters
| Veld | Uitleg | Validatie | Voorbeeld (KVK)                       |
|------|--------|-----------|---------------------------------------|
| **Laagnaam** | Naam van de laag op GeoServer | Optioneel (alleen relevant bij OWS bron) | `null` (niet van toepassing bij REST) |
| **Lijst CQL filters** | CQL (Common Query Language) filters voor het filteren van resultaten bij verzoeken naar een OWS bron voor de lijstweergave. Je kunt template tags gebruiken: `{{variabele}}` | Optioneel (alleen relevant bij OWS bron) | `null` (niet van toepassing bij REST) |
| **Detail CQL filters** | CQL filters voor het filteren van resultaten bij verzoeken naar een OWS bron voor de detailweergave. Je kunt template tags gebruiken: `{{variabele}}` | Optioneel (alleen relevant bij OWS bron) | `null` (niet van toepassing bij REST) |

## Handige tips

### Objectnotatie
Voor het aanspreken van geneste velden gebruik je puntnotatie:
<ul>
<li>Simpel genest veld: object.veld</li>
<li>Diep genest veld: object.subobject.veld</li>
<li>Array element: array[0].veld</li>
</ul>

### Template tags
Voor dynamische waarden in URL's en filters gebruik je dubbele accolades:
<ul>
<li>Enkelvoudig: {{variabele}}</li>
<li>Meerdere: ?postcode={{postcode}}&huisnummer={{huisnummer}}</li>
</ul>

# Voorbeelden

## Voorbeeld configuratie subbuurten tabel (OWS)
Met dit voorbeeld laten we zien hoe je een OWS laag kan configureren.

| Veld                                     | Voorbeeld (subbuurten)                                                |
|------------------------------------------|-----------------------------------------------------------------------|
| **Titel**                                | `Subbuurten`                                                          |
| **Kort kenmerk**                         | `subbuurten`                                                          |
| **Bron**                                 | `https://datalab.purmerend.nl/geoserver/topp/wms`                     |
| **Brontype**                             | `OWS`                                                                 |
| **Beschikbare velden**                   | `subbuurt` `buurt` `wijk`                                             |
| **Toon deze velden in de lijstweergave** | `subbuurt` `buurt` `wijk`                                             |
| **Laagnaam**                             | `topp:grenzen_subbuurten`                                             | 
| **Lijst CQL filters**                    | `[{"key": "wijk", "cql_filter": "wijk in ('{{wijk}}')"}]`             |
| **Detail CQL filters**                   | `[{"key": "subbuurt", "cql_filter": "subbuurt in ('{{subbuurt}}')"}]` |