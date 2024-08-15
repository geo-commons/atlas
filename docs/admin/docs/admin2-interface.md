# De Admin2 interface van Atlas
In dit stuk documentatie staat beschreven hoe de Admin2 interface van Atlas werkt.

## Het gebruiken van Admin2
Admin2 is de nieuwe admin interface voor Atlas, deze interface is beschikbaar door naar ```http://jouwatlasurl.tld/atlas/admin2/``` te navigeren. Wanneer je hier bent aangekomen en ingelogd bent krijg je een dashboard te zien met verschillende tegels. Elk tegel heeft zijn eigen functionaliteit onder zich, waarop wij hieronder verder ingaan. 

## Tegel kaartlagen
Wanneer je de tegel kaartlagen aanklikt krijg je een overzicht te zien in een lijstweergave van kaartlagen die beschikbaar zijn onder jouw Atlas installatie, deze zou je per stuk kunnen bewerken door op de betreffende laag, ofwel het pen icoon te drukken. Daarnaast kan je deze laag verwijderen door op het prullenbak icoon te drukken. Kaartlagen zijn de datasets die binnen Atlas ontsloten worden. Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere kaarten.

### Het bewerken en toevoegen van een kaartlaag
Het bewerken en het toevoegen van een laag werkt in principe hetzelfde, hieronder leggen wij uit wat welk veld exact doet.

#### _Algemene gegevens_
Onder algemene gegevens van de kaartlaag kent Atlas diverse velden, dat zijn de volgende:

**Titel**:
De naam zoals die verschijnt in de legenda van Atlas. 
*Veld eisen*: De invoer mag geen speciale tekens bevatten.

**Kort kenmerk**:
Een uniek kenmerk dat de kaartlaag van de andere kaartlagen onderscheid. Wordt gebruikt als slug voor betreffende kaartlaag.

**Categorie**:
De categorie waar toe de kaartlaag behoort.

**Gepubliceerd**:
Met deze optie bepaal je op de laag wordt gepubliceerd of niet binnen Atlas, deze optie kan gebruikt worden om de laag tijdens het configureren nog niet aan Atlas aan te bieden, of om deze snel (tijdelijk) uit Atlas te verwijderen zonder dat de volledige kaartlaagconfiguratie verwijderd hoeft te worden. *Default*: uit.

#### *Bron*
Onder bron valt de bron informatie van de kaartlaag te configureren, ook hier vallen er weer diverse velden te configureren, dat zijn de volgende:

**Bron**:
Onder het veld bron kan je een keuze maken uit een van de geconfigureerde bronnen binnen Atlas, vanaf deze bron worden de beschikbare laagnamen opgehaald.

**Laagnaam**:
De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bijvoorbeeld: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver.

**Brontype**:
Onder het veld bron specifieer je wat voor brontype (WMS en WFS, WMS, WFS, WMTS, XYZ of MVT) de laag gebruikt. *De laag types*: Een WMS en WFS, of WFS laag is zowel zichtbaar op de kaart als in het datapaneel. WMS, WMTS, MVT en XYZ lagen worden alleen getoond in de kaart.

**Projectie**:
De projectie waarin de kaartlaag bevraagd wordt. *Default*: EPSG:28992.

**Formaat**:
Onder het veld formaat specifieer je wat voor soort afbeelding formaat de bron gebruikt. *Default*: image/png.

#### _Weergave_
Onder weergave vallen alle standaard weergave opties voor de kaartlaag te configureren. 

**Transparantie**:
Onder het veld transparantie configureer je hoe transparent de kaartlaag is. *Veld eisen*: Dit veld kan een waarde hebben tussen de 0 en 1 en één cijfer achter de komma, bijvoorbeeld: Een waarde van 0.1 is goed, een waarde van 0.21 niet. *Default*: 0.9.

**Is basislaag**:
Met het aanzetten van de "is basislaag" optie, zorg je ervoor dat de betreffende kaartlaag de achtergrondkaart wordt. *Default*: uit.

**Is standaard zichtbaar**: 
Met het aanzetten van de "is standaard zichtbaar" optie, zorg je ervoor dat de betreffende kaartlaag standaard zichtbaar wordt. Deze komt bovenop de basislaag. Hierdoor hoeft de eindgebruiker dus niet de kaartlaag handmatig te selecteren om deze zichtbaar te maken. *Default*: uit.

**Is selecteerbaar**:
Met het aanzetten van de "is selecteerbaar" optie, zorg je ervoor dat de betreffende kaartlaag selecteerbaar is en je features op deze kaartlaag kan selecteren. *Default*: aan.

**Haal detailinformatie op als HTML bij de bron**:
Met het aanzetten van de "haal detailinformatie op als HTML bij de bron" optie, zorg je ervoor dat het getFeatureInfo request wat naar betreffende kaartlaag bron wordt gedaan geen JSON data formaat terug verwacht maar een HTML data formaat. *Default*: uit.

**Toon laag in detail- en dataweergave**:
Met het aanzetten van de "toon laag in detail- en dataweergave" optie zorg je ervoor dat de laag zichtbaar is binnen het detail en dataweergave. *Default*: aan.

**Toon laag alleen in een themakaart**:
Met het aanzetten van de "toon laag alleen in een themakaart" optie zorg je ervoor dat de laag alleen zichtbaar wordt binnen themakaarten waarin deze laag specifiek gekozen is, hiermee verdwijnt de laag dus uit het standaard Atlas hoofscherm. *Default*: uit.

**Toon deze velden**:
Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in dit pop-up venster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond. *Veld eisen*: Voer een veld per regel in.

**Doorzoek deze velden**:
Geef in dit veld op door welke velden gezocht kan worden, dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg gelaten wordt, worden alle attributen zoekvelden. *Veld eisen*: Voer een veld per regel in.

**Bereik minimum X**:
Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 123467. *Veld eisen*: Is een geldig RD coordinaat.

**Bereik minimum Y**:
Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 499314. *Veld eisen*: Is een geldig RD coordinaat.

**Bereik maximum X**:
Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 128962. *Veld eisen*: Is een geldig RD coordinaat.

**Bereik maximum Y**:
Vul hier een RD-coordinaat in om de laag inactief te maken wanneer de weergave buiten het bereik ligt van dit RD-coordinaat, bijvoorbeeld: 503402. *Veld eisen*: Is een geldig RD coordinaat.

**Zoomniveau minimum**:
Via het "zoomniveau minimum" veld bepaal je hoe laag het zoomniveau mag zijn voordat de laag niet meer zichtbaar wordt. Bijvoorbeeld: een minimaal zoomniveau van 10, zorgt ervoor dat bij een zoomniveau van 9 de laag niet meer zichtbaar is. *Veld eisen*: Is een heel getal, bijvoorbeeld: 1 of 10, geen 10.5.

**Zoomniveau maximum**:
Via het "zoomniveau maximum" veld bepaal je hoe hoog het zoomniveau mag zijn voordat de laag niet meer zichtbaar wordt. Bijvoorbeeld: een maximaal zoomniveau van 20, zorgt ervoor dat bij een zoomniveau van 21 de laag niet meer zichtbaar is. *Veld eisen*: Is een heel getal, bijvoorbeeld: 1 of 10, geen 10.5.

**Stijlnaam voor WMS / WMTS laag**:
Via het veld "Stijlnaam voor WMS / WMTS laag" is het mogelijk om gebruik te maken van een stijl aanwezig op de GeoServer door exact die naam in dit veld op te nemen. *Veld eisen*: Is de stijlnaam zoals op de GeoServer.

**Stijl voor WFS / MVT laag**:
Door middel van dit veld kan je de standaard GeoServer stijl overschrijven, de inhoud van dit veld moet opgesteld zijn in het GeoStyler formaat. Een voorbeeld:

```json
{
  "name": "GeoStyler Demo",
  "rules": [
    {
      "name": "Rule 1",
      "symbolizers": [
        {
          "kind": "Fill",
          "color": "#0E1058"
        }
      ]
    }
  ]
}
```

Via volgende website kan je zelf gemakkelijk GeoStyler stijlen maken: https://geostyler.github.io/geostyler-demo/.

**Vriendelijke veldnamen**:
Met het vriendelijke veldnamen veld kan je ervoor zorgen dat de uiteindelijke veldnamen die in Atlas worden laten zien een andere naam krijgen dan hoe ze binnen GeoServer gedefinieerd staan. Bijvoorbeeld:

```json
{
  "street_name": "straatnaam"
}
```

Hier is het attribuut ```street_name``` de veldnaam zoals in GeoServer gedefinieerd, de hierbij behorende waarde ```straatnaam``` wordt de uiteindelijke veldnaam die in Atlas wordt getoond. *Veld eisen*: In dit veld moet een geldig JSON formaat opgegeven worden. *Ter informatie*: Lowercase veldnamen krijgen standaard een hoofdletter binnen Atlas. Een liggend streepje (underscore ofwel ```_```) wordt omgezet naar een spatie.

**Templatevelden**:
TODO: Dit veld moet nog worden voorzien van de juiste documentatie.

**Legenda**:
Met het "legenda" veld kan je de legenda link die gebruikt wordt binnen Atlas om de uiteindelijke legenda afbeelding voor de kaartlaag op te halen overschrijven. Bijvoorbeeld: https://example.com/picture.jpg, zorgt ervoor dat de legenda afbeelding voor bijbehorende kaartlaag voortaan vanaf deze URL wordt opgehaald. *Veld eisen*: De link moet altijd een link naar een afbeelding zijn, example.com/image kan niet, example.com/image.png kan wel.

#### *Metadata*:
Onder metadata kunnen alle metadata gerelateerde velden worden geconfigureerd. Veel van deze metadata is zichtbaar in Atlas wanneer je via het "Zichtbare lagen" menu naar de kaartlaag zelf navigeert en hier op het "i" icoon drukt.

**Naam**:
Vul een metadata naam in, bijvoorbeeld: Voor de scholenkaart kan de naam "alle type onderwijs" gekozen worden.

**Omschrijving**: Vul een metadata omschrijving in. Bijvoorbeeld: "De kaart is nog in bewerking" of "oude scholenkaart van 1980". *Ter informatie*: Er kan markdown in dit veld gebruikt worden. 

**Organisatie**: Vul in tot welke organisatie de data behoort. Bijvoorbeeld "Gemeente Purmerend".

**Contactpersoon**: Vul hier de contactpersoon in waarmee contact opgenomen kan worden bij vragen over de kaartlaag en/of data. 

**Herkomst van data**: Vul hier in wat de herkomst van de data is. *Ter informatie*: Er kan markdown in dit veld gebruikt worden.

**Laatst bijgewerkt**: Vul hier de datum in die overeenkomt met de datum waarop de kaartlaag en/of data voor het laatst bijgewerkt is. *Veld eisen*: Dit moet een geldige datum zijn.

**Meer informatie**: Vul hier een link naar een metadatacatalogus in. *Veld eisen*: Moet een geldige link zijn.

#### *Toegang*
Via toegang valt te regelen wie wel en geen toegang hebben tot het zien van een kaartlaag, ga hier zorgvuldig mee om.

**Alleen intern zichtbaar**: Wanneer "alleen intern zichtbaar" aan staat, is betreffende kaartlaag alleen beschikbaar binnen de interne omgeving. *Default*: aan.

**Vereis inlog voor deze dataset**: Wanneer "vereis inlog voor deze dataset" aan staat, is betreffende kaartlaag alleen beschikbaar voor personen die zijn ingelogd binnen de Atlas omgeving. Indien je niet ingelogd bent verschijnt de kaartlaag wel in het overzicht van lagen, maar krijg je de kaartlaag niet te zien en zie je enkel een slotje bij de kaartlaag staan om aan te wijzen dat je moet inloggen.

**Groepen**: Onder "beschikbare groepen" staat een lijst met groepen die beschikbaar zijn binnen de Atlas omgeving, onder "geselecteerde groepen" staat een lijst met groepen die toegang hebben tot de kaartlaag.

