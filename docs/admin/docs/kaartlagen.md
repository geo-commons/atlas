Kaartlagen zijn de datasets die binnen Atlas ontsloten worden.
Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere kaarten.

Klik op Nieuwe laag in het kaartlagen scherm om een nieuwe kaartlaag aan te maken.  
Vul de drie velden in en klik daarna op Opslaan en openen om de nieuwe kaartlaag te configureren.

- **Titel** is het veld dat getoond gaat worden in het kaartlagenmenu van Atlas. De invoer mag geen 'speciale' tekens bevatten.
- [**Categorie**](categorie.md) is de groep waaronder de kaartlaag zichtbaar zal zijn in het kaartlagenmenu van Atlas. Kies hier vanuit het pull-down menu een categorie.
- [**Bron**](bronnen.md) is een eerder aangemaakt endpoint waarvanuit de laag geserveerd wordt. Dit kan vanuit een eigen Geoserver zijn maar ook een externe bron.

<img src="../images/configureer_nieuwe_kaartlaag.png" alt="Kaart Toevoegen" width="700"/>

In het kaartlaagmenu kunnen nu de overige kaartlaagsettings ingevuld worden.

### Algemene gegevens

Onder algemene gegevens van de kaartlaag kent Atlas diverse velden, dat zijn de volgende:

- **Titel**
- **Kort kenmerk:** (Een uniek ID dat de layer onderscheid van andere. Wordt gebruikt als slug voor betreffende kaartlaag.
- **Categorie:** De categorie waar toe de kaartlaag behoort. (selecteer onder welke categorie deze layer komt)
- **Metadataset:** Selecteer de metadataset die aan deze kaartlaag gekoppeld moet worden. De metadataset bevat alle metadata informatie conform ISO 19115 standaard. Deze koppeling is verplicht voor publicatie van de kaartlaag.

!!! info "Publicatie vereiste"
Een kaartlaag kan alleen worden gepubliceerd als er een metadataset aan is gekoppeld. Dit is nodig zodat gebruikers altijd toegang hebben tot de juiste beschrijvende informatie (metadata) over de kaartlaag. Zonder gekoppelde metadataset ontbreekt deze informatie en voldoet de publicatie niet aan de kwaliteits- en transparantie-eisen.

- **Gepubliceerd:** Met deze optie bepaal je op de laag wordt gepubliceerd of niet binnen Atlas, deze optie kan gebruikt worden om de laag tijdens het configureren nog niet aan Atlas aan te bieden, of om deze snel (tijdelijk) uit Atlas te verwijderen zonder dat de volledige kaartlaagconfiguratie verwijderd hoeft te worden. _Standaard_: uit.
- **Kaartlaag is exporteerbaar**: Met deze optie bepaal je of de data achter de kaartlaag wel of niet exporteerbaar is vanuit de dataweergave. _Standaard_: aan.

### Bron

Onder bron valt de bron informatie van de kaartlaag te configureren, ook hier vallen er weer diverse velden te configureren, dat zijn de volgende:

- **Bron:** Selecteer er één zoals die bij 'Bronnen' zijn geconfigureerd .Onder het veld bron kan je een keuze maken uit een van de geconfigureerde bronnen binnen Atlas, vanaf deze bron worden de beschikbare laagnamen opgehaald.
- **Laagnaam:** De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bv: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver. Indien je de CRUD functionaliteit wil gebruiken voor de kaartlaag is het van belang altijd de GeoServer omgeving in de naam op te nemen.
- **Brontype:** Onder het veld bron specifieer je wat voor brontype (WMS en WFS, WMS, WFS, WMTS, XYZ of MVT) de laag gebruikt. _De laag types_: Een WMS en WFS, of WFS laag is zowel zichtbaar op de kaart als in het datapaneel. WMS, WMTS, MVT en XYZ lagen worden alleen getoond in de kaart.
- **Projectie:** De projectie waarin de kaartlaag bevraagd wordt. Default: EPSG:28992
- **Server type:** _standaard:_ geoserver

### Weergave

Onder weergave vallen alle standaard weergaveopties voor de kaartlaag te configureren.

- **Transparantie:** Onder het veld transparantie configureer je hoe transparent de kaartlaag is. _Veld eisen_: Dit veld kan een waarde hebben tussen de 0 en 1 en één cijfer achter de komma, bijvoorbeeld: Een waarde van 0.1 is goed, een waarde van 0.21 niet. _Standaard_: 0.9.

- **Is basislaag:** Met het aanzetten van de "is basislaag" optie, zorg je ervoor dat de betreffende kaartlaag de achtergrondkaart wordt. _Standaard_: uit.
- **Is standaard zichtbaar:** Met het aanzetten van de "is standaard zichtbaar" optie, zorg je ervoor dat de betreffende kaartlaag standaard zichtbaar wordt. Deze komt bovenop de basislaag. Hierdoor hoeft de eindgebruiker dus niet de kaartlaag handmatig te selecteren om deze zichtbaar te maken. _Standaard_: uit.
- **Is selecteerbaar:** Met het aanzetten van de "is selecteerbaar" optie, zorg je ervoor dat de betreffende kaartlaag selecteerbaar is en je features op deze kaartlaag kan selecteren. _Standaard_: aan.
- **Haal detailinformatie als HTML op bij de bron:** Met het aanzetten van de "haal detailinformatie op als HTML bij de bron" optie, zorg je ervoor dat het getFeatureInfo request wat naar betreffende kaartlaag bron wordt gedaan geen JSON-data formaat terugverwacht maar een HTML-data formaat. _Standaard_: uit.
- **Toon laag in detail- en dataweergave:** Met het aanzetten van de "toon laag in detail- en dataweergave" optie zorg je ervoor dat de laag zichtbaar is binnen het detail en dataweergave. _Standaard_: aan.
- **Toon laag alleen in een themakaart:** Met het aanzetten van de "toon laag alleen in een themakaart" optie zorg je ervoor dat de laag alleen zichtbaar wordt binnen themakaarten waarin deze laag specifiek gekozen is, hiermee verdwijnt de laag dus uit het standaard Atlas hoofscherm. _Standaard_: uit.
- **Laag is filterbaar in legenda:** Met het aanzetten van de "Laag is filterbaar in legenda" optie zorg je ervoor dat op deze laag de legenda filterbaar wordt. Let op: Deze functie werkt enkel met WMS, WMS-WFS en WFS bronnen die een JSON response ondersteunen. _Standaard_: uit.
- **Kan doorzocht worden:** (maak het mogelijk de laag te bevragen door in de kaart te klikken (popup attriutes) én maak de layer zichtbaar in de zoekfunctie )
- **Toon deze velden:** ([Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in dit pop-up venster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond.)ij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in het pop-upvenster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond. _Veld eisen_: Voer een veld per regel in.
- **Doorzoek deze velden:** Geef in dit veld op door welke velden gezocht kan worden, dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg gelaten wordt, worden alle attributen zoekvelden. _Veld eisen_: Voer een veld per regel in.

**Bereik minimum en maximum** kunnen ingevuld worden om een bounding-box te configureren. Dit kan handig zijn wanneer een kaartlaag maar één of een paar objecten toont die dicht bij elkaar liggen, er kan dan direct ingezoomd worden naar dit gebied. Bovendien zal de laag inactief gemaakt worden wanneer de weergave buiten het bereik ligt van de bounding box.
Een geldig RD coördinaat is bijvoorbeeld: _128981.03_

- **Bereik minimum x:** Dit is de X waarde van het coördinaat linksonder. _Veld eisen_: Is een geldig RD coordinaat.
- **Bereik minimum y:** Dit is de Y waarde van het coördinaat linksonder. _Veld eisen_: Is een geldig RD coordinaat.
- **Bereik maximum x:** Dit is de X waarde van het coördinaat rechtsboven. _Veld eisen_: Is een geldig RD coordinaat.
- **Bereik maximum y:** Dit is de Y waarde van het coördinaat rechtsboven. _Veld eisen_: Is een geldig RD coordinaat.

- **Zoomniveau minimum:** Wanneer in het stijlbestand (SLD) [MinScaleDenominator](https://docs.geoserver.org/main/en/user/styling/sld/reference/rules.html) en/of [MaxScaleDenominator](https://docs.geoserver.org/main/en/user/styling/sld/reference/rules.html) geconfigureerd is voor een object, dan is het raadzaam zoomniveau minimum en/of zoomniveau maximum in te vullen.
  Wanneer het zoomniveau wordt ingevuld zal de kaartlaag greyed-out worden wanneer te ver uitgezoomd (minimum) of te ver inzoomd (maximum) is. Wanneer de kaartlaag greyed-out is verschijnt een vergrootglas-icoon naast de kaartlaagnaam. Klikken hierop laat de kaartlaag in- of uitzoomen naar het niveau waar de objecten getoond worden.

Via het "zoomniveau minimum" veld bepaal je wat het minimale zoomniveau is waarbij de objecten binnen de laag niet meer zichtbaar zijn (Hoe verder uitgezoomd wordt, hoe kleiner het zoomniveau). Bijvoorbeeld: een minimaal zoomniveau van 10, zorgt ervoor dat bij een zoomniveau van 9 de objecten niet meer zichtbaar zijn. _Veld eisen_: Numeriek. Nauwkeurigheid: 2 cijfers achter de komma, bijvoorbeeld: 10,55. Wanneer een punt wordt ingegeven, wordt dez automatisch omgezet naar een komma.

- **Zoomniveau maximum:** Via het "zoomniveau maximum" veld bepaal je wat het maximale zoomniveau is waarbij de objecten binnen de laag nog zichtbaar zijn (Hoe verder ingezoomd wordt, hoe groter het zoomniveau). Bijvoorbeeld: een maximaal zoomniveau van 21, zorgt ervoor dat bij een zoomniveau van 22 de objecten niet meer zichtbaar zijn. _Veld eisen_: Numeriek. Nauwkeurigheid: 2 cijfers achter de komma, bijvoorbeeld: 20,55. Wanneer een punt wordt ingegeven, wordt dez automatisch omgezet naar een komma.

!!! info

    Het zoomniveau is dus omgekeerd aan de schaalwaarde. Bij inzoomen wordt de schaal kleiner maar het zoomniveau groter. Dit kan verwarrend zijn bij het configureren van bovenstaande waardes.
    Een handvat:

    Zoomniveau MaxScaleDenominator Niveau

    12,96      70000               Regio-overzicht
    14,48      24000               Stadsniveau
    19,5       1000                Straatniveau
    22,34      100                 Huis/perceelniveau

!!! tip

    De MinScaleDenominator en MaxScaleDenominator waardes komen overeen met de schaallat rechtsonderin het Atlas kaartscherm. Klik eventueel 1x op de schaallat om in de schaalmodus te komen.
    Het zoomniveau kan uit de url gehaald worden:
    https://hostnaam.nl/atlas/@126647.71,501835.21,16.02z/layers=id_mijn_layer/base=achtergrondkaart
    Het zoomniveau staat hier achter de coordinaten, dus 16.02.

- **Stijlnaam voor WMS / WMTS laag:** m verschillende stijlen met één kaartlaag te kunnen gebruiken, kan hier een stijlbestand worden ingevuld. Het stijlbestand waarmee de kaartlaag in Geoserver is geconfigureerd wordt hiermee overruled. Het stijlbestand dat hier wordt ingevuld moet net als het originele stijlbestand op de Geoserver staan.
  Via het veld "Stijlnaam voor WMS / WMTS laag" is het mogelijk om gebruik te maken van een stijl aanwezig op de GeoServer door exact die naam in dit veld op te nemen. _Veld eisen_: Is de stijlnaam zoals op de GeoServer. Hiermee wordt de WFS stijl in Geoserver overruled.

- **Stijl voor WFS / MVT laag:** m verschillende stijlen met één kaartlaag te kunnen gebruiken, kan hier een stijlbestand worden ingevuld. Het stijlbestand waarmee de kaartlaag in Geoserver is geconfigureerd wordt hiermee overruled. Het stijlbestand dat hier wordt ingevuld moet net als het originele stijlbestand op de Geoserver staan.
  Door middel van dit veld kan je de standaard GeoServer stijl overschrijven, de inhoud van dit veld moet opgesteld zijn in het GeoStyler formaat. Via [de GeoStyler website](https://geostyler.github.io/geostyler-demo/) kan je zelf gemakkelijk stijlen maken.

- **Vriendelijke veldnamen:** Met het vriendelijke veldnamen veld kan je ervoor zorgen dat de uiteindelijke veldnamen die in Atlas worden laten zien een andere naam krijgen dan hoe ze binnen GeoServer gedefinieerd staan. Bijvoorbeeld:

```json
{
  {"street_name": "straatnaam", "postc": "Postcode"}
}
```

!!! warning "Waarschuwing"

    Wanneer JSON formaat gekopieerd wordt (bijvoorbeeld bovenstaande code naar Atlas), dan kan de characterset veranderen. Dit zorgt ervoor dat aanhalingstekens niet herkent worden en de code niet geaccepteerd wordt.

!!! info

    Overigens krijgen lowercase veldnamen standaard een hoofdletter binnen Atlas. Een liggend streepje (underscore) wordt omgezet naar een spatie.

- **Templatevelden:** Met templatevelden is het mogelijk om nieuwe velden toe te voegen aan een kaartlaag. Dit kun je bijvoorbeeld gebruiken om een samengesteld veld _adres_ te maken, waarin de velden _straatnaam_ en _huisnummer_ worden samengevoegd. Je gebruikt hiervoor een JSON structuur, waarbij de sleutel de naam van het veld is, en de waarde de template die gerender wordt. Bijvoorbeeld:

```json
{
  "adres": "{{ properties.straatnaam }} {{ properties.huisnummer }}"
}
```

- **Legenda:** Met het "legenda" veld kan je de legenda link die gebruikt wordt binnen Atlas om de uiteindelijke legenda afbeelding voor de kaartlaag op te halen overschrijven. Bijvoorbeeld: https://example.com/picture.jpg, zorgt ervoor dat de legenda afbeelding voor bijbehorende kaartlaag voortaan vanaf deze URL wordt opgehaald. _Veld eisen_: De link moet altijd een link naar een afbeelding zijn, example.com/image kan niet, example.com/image.png kan wel.

- **Zoektermen:** Via het veld "Zoektermen" kun je extra termen opgeven waarop een kaartlaag gevonden kan worden bij gebruik van de zoekfunctie binnen Atlas. Dit is vooral handig wanneer gebruikers verschillende woorden gebruiken voor hetzelfde concept. Bijvoorbeeld: bij een kaartlaag met als titel Scholen kun je de zoektermen onderwijs, educatie en basisschool toevoegen, zodat gebruikers deze kaartlaag ook vinden wanneer ze op die alternatieve termen zoeken. Voeg één zoekterm per regel in.

### Toegang

Via toegang valt te regelen wie wel en geen toegang hebben tot het zien van een kaartlaag, ga hier zorgvuldig mee om.

- **Alleen intern zichtbaar:** Wanneer "alleen intern zichtbaar" aan staat, is betreffende kaartlaag alleen beschikbaar binnen de interne omgeving. _Standaard_: aan.
- **Vereis inlog voor deze kaartlaag:** Wanneer "vereis inlog voor deze kaartlaag" aan staat, is betreffende kaartlaag alleen beschikbaar voor personen die zijn ingelogd binnen de Atlas omgeving. Indien je niet ingelogd bent, verschijnt de kaartlaag wel in het overzicht van lagen, maar krijg je de kaartlaag niet te zien en zie je enkel een slotje bij de kaartlaag staan om aan te wijzen dat je moet inloggen.
  - **Ingelogde gebruikers kunnen kaartlaag bewerken:**
    Wanneer deze optie is ingeschakeld, kunnen alle ingelogde gebruikers binnen Atlas objecten op de kaartlaag muteren, dat wil zeggen: **toevoegen**, **bewerken** en/of **verwijderen**. Dit kan via zowel de kaartlaag module als de autorisatie module geregeld worden.

    Wil je dat gebruikers deze acties kunnen uitvoeren, dan zijn er twee mogelijkheden:
    1. **Schakel deze optie in**  
       Hiermee krijgen alle ingelogde gebruikers bewerkingsrechten op de kaartlaag.

    2. **Gebruik schrijfgroepen**  
       In plaats van algemene toegang kun je specifieke gebruikers of groepen schrijfrechten geven via:
       - De instellingen van de **kaartlaag**
       - De instellingen binnen de **autorisatie**-module

    > 💡 Tip: Gebruik schrijfgroepen als je meer controle wilt over wie wijzigingen mag aanbrengen.

- **Lees groepen:** Onder "beschikbare groepen" staat een lijst met groepen die beschikbaar zijn binnen de Atlas omgeving, onder "geselecteerde groepen" staat een lijst met groepen die toegang hebben tot de kaartlaag.
- **Schrijf groepen:** Onder "schrijf groepen" staat een lijst met groepen die beschikbaar zijn binnen de Atlas omgeving, onder "geselecteerde groepen" staat een lijst met groepen die toegang hebben tot het muteren van objecten op de kaartlaag (toevoegen, bewerken en/of verwijderen van objecten).

## Relaties tussen kaartlaag en tabellen

Een kracht van tabellen is dat je ze kan verbinden aan kaartlagen, waardoor je in de detailweergave van een object op een kaartlaag de lijstweergaves van andere tabellen kan tonen. Dit noemen wij ook wel een relatie tussen kaartlaag en tabellen.

### Het configureren van een relatie

Voeg een nieuwe relatie toe door op "Nieuwe relatie" te drukken. Kies een tabel die je wil koppelen aan de huidige kaartlaag en klik op "Toevoegen". Nu zie je dat er een relatie voor de kaartlaag is toegevoegd. Via het veld "Field Mapping" configureer je welke velden uit de huidige kaartlaag kunnen worden gebruikt om data op te vragen in de gerelateerde tabel.

**Een voorbeeld:**
<img src="../images/gerelateerde-tabel.png" alt="Voorbeeld van geconfigureerde relatie" width="800"/>

In het bovenstaande voorbeeld zie je dat het veld "wijknaam" vanuit de huidige kaartlaag wordt gemapped naar het veld "wijk" van de gerelateerde tabel.

In de gerelateerde tabel kan hierna het veld "wijk" worden gebruiken in het "Lijst endpoint" veld of in het "Lijst CQL filters" veld.

Je kan meerdere field mapping waardes toevoegen, dit object dient geldige JSON te zijn. Bijvoorbeeld:

```json
{
  "wijknaam": "wijk",
  "buurtnaam": "buurt",
  "straatnaam": "straat",
  "nummer": "huisnummer"
}
```

### (Oud) Gekoppelde Data

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

### (Oud) Templates

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

Sla de gegevens op na het aanmaken van een gekoppelde laag.
