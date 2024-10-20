# Nieuw beheerpaneel

## Kaartlaag

### Algemene gegevens

Onder algemene gegevens van de kaartlaag kent Atlas diverse velden, dat zijn de volgende:

- _Titel_ De naam zoals die verschijnt in de legenda van Atlas. _Veld eisen_: De invoer mag geen speciale tekens bevatten.
- _Kort kenmerk_: Een uniek kenmerk dat de kaartlaag van de andere kaartlagen onderscheid. Wordt gebruikt als slug voor betreffende kaartlaag.
- _Categorie_: De categorie waar toe de kaartlaag behoort.
- _Gepubliceerd_: Met deze optie bepaal je op de laag wordt gepubliceerd of niet binnen Atlas, deze optie kan gebruikt worden om de laag tijdens het configureren nog niet aan Atlas aan te bieden, of om deze snel (tijdelijk) uit Atlas te verwijderen zonder dat de volledige kaartlaagconfiguratie verwijderd hoeft te worden. _Standaard_: uit.

### Bron

Onder bron valt de bron informatie van de kaartlaag te configureren, ook hier vallen er weer diverse velden te configureren, dat zijn de volgende:

- _Bron_: Onder het veld bron kan je een keuze maken uit een van de geconfigureerde bronnen binnen Atlas, vanaf deze bron worden de beschikbare laagnamen opgehaald.
- _Laagnaam_: De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bijvoorbeeld: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver.
- _Brontype_: Onder het veld bron specifieer je wat voor brontype (WMS en WFS, WMS, WFS, WMTS, XYZ of MVT) de laag gebruikt. _De laag types_: Een WMS en WFS, of WFS laag is zowel zichtbaar op de kaart als in het datapaneel. WMS, WMTS, MVT en XYZ lagen worden alleen getoond in de kaart.
- _Projectie_: De projectie waarin de kaartlaag bevraagd wordt. _Standaard_: EPSG:28992.
- _Formaat_: Onder het veld formaat specifieer je wat voor soort afbeelding formaat de bron gebruikt. _Standaard_: image/png.

### Weergave

#### Basisopties

Onder weergave vallen alle standaard weergave opties voor de kaartlaag te configureren.

- _Transparantie_: Onder het veld transparantie configureer je hoe transparent de kaartlaag is. _Veld eisen_: Dit veld kan een waarde hebben tussen de 0 en 1 en één cijfer achter de komma, bijvoorbeeld: Een waarde van 0.1 is goed, een waarde van 0.21 niet. _Standaard_: 0.9.
- _Is basislaag_: Met het aanzetten van de "is basislaag" optie, zorg je ervoor dat de betreffende kaartlaag de achtergrondkaart wordt. _Standaard_: uit.
- _Is standaard zichtbaar_: Met het aanzetten van de "is standaard zichtbaar" optie, zorg je ervoor dat de betreffende kaartlaag standaard zichtbaar wordt. Deze komt bovenop de basislaag. Hierdoor hoeft de eindgebruiker dus niet de kaartlaag handmatig te selecteren om deze zichtbaar te maken. _Standaard_: uit.
- _Is selecteerbaar_: Met het aanzetten van de "is selecteerbaar" optie, zorg je ervoor dat de betreffende kaartlaag selecteerbaar is en je features op deze kaartlaag kan selecteren. _Standaard_: aan.
- _Haal detailinformatie op als HTML bij de bron_: Met het aanzetten van de "haal detailinformatie op als HTML bij de bron" optie, zorg je ervoor dat het getFeatureInfo request wat naar betreffende kaartlaag bron wordt gedaan geen JSON-data formaat terugverwacht maar een HTML-data formaat. _Standaard_: uit.
- _Toon laag in detail- en dataweergave_: Met het aanzetten van de "toon laag in detail- en dataweergave" optie zorg je ervoor dat de laag zichtbaar is binnen het detail en dataweergave. _Standaard_: aan.
- _Toon laag alleen in een themakaart_: Met het aanzetten van de "toon laag alleen in een themakaart" optie zorg je ervoor dat de laag alleen zichtbaar wordt binnen themakaarten waarin deze laag specifiek gekozen is, hiermee verdwijnt de laag dus uit het standaard Atlas hoofscherm. _Standaard_: uit.
- _Toon deze velden_: Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in het pop-upvenster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond. _Veld eisen_: Voer een veld per regel in.
- _Doorzoek deze velden_: Geef in dit veld op door welke velden gezocht kan worden, dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg gelaten wordt, worden alle attributen zoekvelden. _Veld eisen_: Voer een veld per regel in.
- _Bereik minimum X_: Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 123467. _Veld eisen_: Is een geldig RD coordinaat.
- _Bereik minimum Y_: Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 499314. _Veld eisen_: Is een geldig RD coordinaat.
- _Bereik maximum X_: Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 128962. _Veld eisen_: Is een geldig RD coordinaat.
- _Bereik maximum Y_: Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 503402. _Veld eisen_: Is een geldig RD coordinaat.
- _Zoomniveau minimum_: Via het "zoomniveau minimum" veld bepaal je hoe laag het zoomniveau mag zijn voordat de laag niet meer zichtbaar wordt. Bijvoorbeeld: een minimaal zoomniveau van 10, zorgt ervoor dat bij een zoomniveau van 9 de laag niet meer zichtbaar is. _Veld eisen_: Is een heel getal, bijvoorbeeld: 1 of 10, geen 10.5.
- _Zoomniveau maximum_: Via het "zoomniveau maximum" veld bepaal je hoe hoog het zoomniveau mag zijn voordat de laag niet meer zichtbaar wordt. Bijvoorbeeld: een maximaal zoomniveau van 20, zorgt ervoor dat bij een zoomniveau van 21 de laag niet meer zichtbaar is. _Veld eisen_: Is een heel getal, bijvoorbeeld: 1 of 10, geen 10.5.

#### Stijlnaam voor WMS / WMTS laag

Via het veld "Stijlnaam voor WMS / WMTS laag" is het mogelijk om gebruik te maken van een stijl aanwezig op de GeoServer door exact die naam in dit veld op te nemen. _Veld eisen_: Is de stijlnaam zoals op de GeoServer.

#### Stijl voor WFS / MVT laag

Door middel van dit veld kan je de standaard GeoServer stijl overschrijven, de inhoud van dit veld moet opgesteld zijn in het GeoStyler formaat. Via [de GeoStyler website](https://geostyler.github.io/geostyler-demo/) kan je zelf gemakkelijk stijlen maken.

#### Vriendelijke veldnamen

Met het vriendelijke veldnamen veld kan je ervoor zorgen dat de uiteindelijke veldnamen die in Atlas worden laten zien een andere naam krijgen dan hoe ze binnen GeoServer gedefinieerd staan. Bijvoorbeeld:

```json
{
  "street_name": "straatnaam"
}
```

Hier is het attribuut `street_name` de veldnaam zoals in GeoServer gedefinieerd, de hierbij behorende waarde `straatnaam` wordt de uiteindelijke veldnaam die in Atlas wordt getoond. _Veld eisen_: In dit veld moet een geldig JSON-formaat opgegeven worden. _Ter informatie_: Lowercase veldnamen krijgen standaard een hoofdletter binnen Atlas. Een liggend streepje (underscore ofwel `_`) wordt omgezet naar een spatie.

#### Templatevelden

Met templatevelden is het mogelijk om nieuwe velden toe te voegen aan een kaartlaag. Dit kun je bijvoorbeeld gebruiken om een samengesteld veld _adres_ te maken, waarin de velden _straatnaam_ en _huisnummer_ worden samengevoegd. Je gebruikt hiervoor een JSON structuur, waarbij de sleutel de naam van het veld is, en de waarde de template die gerender wordt. Bijvoorbeeld:

```json
{
  "adres": "{{ properties.straatnaam }} {{ properties.huisnummer }}"
}
```

#### Legenda

Met het "legenda" veld kan je de legenda link die gebruikt wordt binnen Atlas om de uiteindelijke legenda afbeelding voor de kaartlaag op te halen overschrijven. Bijvoorbeeld: https://example.com/picture.jpg, zorgt ervoor dat de legenda afbeelding voor bijbehorende kaartlaag voortaan vanaf deze URL wordt opgehaald. _Veld eisen_: De link moet altijd een link naar een afbeelding zijn, example.com/image kan niet, example.com/image.png kan wel.

### Metadata

Onder metadata kunnen alle metadata gerelateerde velden worden geconfigureerd. Veel van deze metadata is zichtbaar in Atlas wanneer je via het "Zichtbare lagen" menu naar de kaartlaag zelf navigeert en hier op het "i" icoon drukt.

- _Naam_: Vul een metadata naam in, bijvoorbeeld: Voor de scholenkaart kan de naam "alle type onderwijs" gekozen worden.
- _Omschrijving_: Vul een metadata omschrijving in. Bijvoorbeeld: "De kaart is nog in bewerking" of "oude scholenkaart van 1980". _Ter informatie_: Er kan markdown in dit veld gebruikt worden.
- _Organisatie_: Vul in tot welke organisatie de data behoort. Bijvoorbeeld "Gemeente Purmerend".
- _Contactpersoon_: Vul hier de contactpersoon in waarmee contact opgenomen kan worden bij vragen over de kaartlaag en/of data.
- _Herkomst van data_: Vul hier in wat de herkomst van de data is. _Ter informatie_: Er kan markdown in dit veld gebruikt worden.
- _Laatst bijgewerkt_: Vul hier de datum in die overeenkomt met de datum waarop de kaartlaag en/of data voor het laatst bijgewerkt is. _Veld eisen_: Dit moet een geldige datum zijn.
- _Meer informatie_: Vul hier een link naar een metadatacatalogus in. _Veld eisen_: Moet een geldige link zijn.

### Toegang

Via toegang valt te regelen wie wel en geen toegang hebben tot het zien van een kaartlaag, ga hier zorgvuldig mee om.

- _Alleen intern zichtbaar_: Wanneer "alleen intern zichtbaar" aan staat, is betreffende kaartlaag alleen beschikbaar binnen de interne omgeving. _Standaard_: aan.
- _Vereis inlog voor deze dataset_: Wanneer "vereis inlog voor deze dataset" aan staat, is betreffende kaartlaag alleen beschikbaar voor personen die zijn ingelogd binnen de Atlas omgeving. Indien je niet ingelogd bent, verschijnt de kaartlaag wel in het overzicht van lagen, maar krijg je de kaartlaag niet te zien en zie je enkel een slotje bij de kaartlaag staan om aan te wijzen dat je moet inloggen.
- _Groepen_: Onder "beschikbare groepen" staat een lijst met groepen die beschikbaar zijn binnen de Atlas omgeving, onder "geselecteerde groepen" staat een lijst met groepen die toegang hebben tot de kaartlaag.

### Gekoppelde data

Met gekoppelde data is het mogelijk om een tabelweergave te tonen met gekoppelde data bij de detailweergave van een feature. Deze data komt uit een OWS bron (WMS/WFS). Denk bijvoorbeeld aan het tonen van alle adressen bij een BAG pand. Het is mogelijk om meerdere tabellen te koppelen bij één punt.

Per tabel zijn er de volgende instellingen:

- _Titel_: de naam van de tabel aan de voorkant
- _Laag_: de naam van de laag in de Geobron
- _URL_: de URL naar de OWS service van de geo-bron (WMS/WFS)
- _Bronsleutel_: het veld waarmee gekoppeld wordt in de bronlaag (de laag die op de kaart toont)
- _Doelsleutel_: het veld waarmee gekoppeld wordt in de doellaag (de laag die getoond wordt in de tabel)
- _Tabel kopjes_: overschrijf de tabel met eigen kopje (optioneel)
- _Toon deze velden_: beperk de tabel met vooringestelde velden. Dit is een lijst met velden, gesplitst door een enter (optioneel)
- _Gebruik detailweergave_: maak het mogelijk om door te klikken op een rij in de tabel en hier een detailweergave voor te tonen (optioneel)
- _Toon deze velden in de detailweergave_: beperk de detailweergave met vooringestelde velden. Dit is een lijst met velden, gesplitst door een enter

### Templates

Met templates is het mogelijk om een tabelweergave of een veldweergave te tonen met gekoppelde data bij de detailweergave van een feature. Deze data komt uit een REST bron. Denk bijvoorbeeld aan het tonen van alle vestigingen uit het handelsregister bij een specifiek BAG-adres.

Per template zijn de volgende instellingen:

- _Bron_: de bron in Atlas
- _Endpoint_: het REST endpoint dat bevraagd wordt
- _Methode_: de REST methode die gebruikt wordt
- _Titel_: de naam van de tabel aan de voorkant
- _Tabel veld met lijst_: het veld in het HTTP response dat gebruikt wordt voor de lijstweergave
- _Tabel kopjes_: de kopjes van de tabel
- _Toon deze velden_: de velden van de tabel
- _Vrij veld template_: gebruik dit veld om géén tabelweergave maar een vrij template te tonen (optioneel)
