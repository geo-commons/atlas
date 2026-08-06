Kaarten zijn verzamelingen van kaartlagen die samen een onderwerp vormen. Een kaart is in Atlas een configureerbare viewer met een eigen selectie lagen, eigen kaartinstellingen en eigen functionaliteit.

Ook de **hoofdkaart** is een kaart. Het verschil is dat de hoofdkaart de standaardkaart van Atlas is:

- de hoofdkaart is bereikbaar via `/atlas/`
- de hoofdkaart is altijd gepubliceerd
- de hoofdkaart wordt niet in het dataportaal getoond
- de hoofdkaart kan niet worden verwijderd
- de hoofdkaart is configureerbaar via een losse knop op het admin dashboard

Een thematische kaart is bereikbaar via een eigen URL, bijvoorbeeld:
`https://mijngemeentewebsite.nl/atlas/maps/hondenbeleid`

<img src="../images/hondenbeleid.png" alt="hondenbeleid" width="500"/>

Om een kaart aan te maken klik je in het menu **Kaarten** op **Nieuwe kaart**. Vul de verplichte velden in en klik op **Opslaan en openen**.

## Kaartinstellingen

In het kaartmenu kunnen de verschillende onderdelen van een kaart worden ingesteld. Aangevinkte opties zijn direct zichtbaar in het voorbeeldscherm.

### Algemene instellingen

| Veld                              | Uitleg                                                                                                                                     | Opmerking                                                                         |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **Titel**                         | De titel van de kaart. Deze naam wordt in Atlas getoond.                                                                                   | Verplicht. Niet instelbaar voor de hoofdkaart.                                    |
| **Kort kenmerk**                  | Een korte, unieke naam voor de kaart die in de URL wordt gebruikt. Gebruik geen spaties of speciale tekens. Streepjes zijn wel toegestaan. | Verplicht, uniek. Niet instelbaar voor de hoofdkaart.                             |
| **Portaal beschrijving**          | De beschrijving van de kaart zoals die in het dataportaal wordt getoond.                                                                   | Optioneel. Niet instelbaar voor de hoofdkaart.                                    |
| **Zoektermen**                    | Zoektermen waarmee de kaart in het dataportaal gevonden kan worden. Voer een zoekterm per regel in.                                        | Optioneel. Niet instelbaar voor de hoofdkaart.                                    |
| **Centrum X-coördinaat**          | Het X-coördinaat van de startpositie van de kaart.                                                                                         | Overschrijft voor deze kaart de globale standaardpositie.                         |
| **Centrum Y-coördinaat**          | Het Y-coördinaat van de startpositie van de kaart.                                                                                         | Overschrijft voor deze kaart de globale standaardpositie.                         |
| **Zoomniveau**                    | Het zoomniveau waarmee de kaart opent.                                                                                                     | Overschrijft voor deze kaart het globale standaardzoomniveau.                     |
| **Publiceer kaart**               | Publiceert de kaart zodat deze beschikbaar is voor gebruikers.                                                                             | Alleen zichtbaar bij thematische kaarten. Bij de hoofdkaart altijd ingeschakeld.  |
| **Toon kaart in het dataportaal** | Bepaalt of de kaart zichtbaar is in het overzicht van het dataportaal.                                                                     | Alleen zichtbaar bij thematische kaarten. Bij de hoofdkaart altijd uitgeschakeld. |

### Onderdelen van de kaart

| Onderdeel                                   | Uitleg                                                           | Opmerking                                                           |
| ------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------- |
| [**Lagen**](#lagen)                         | Hier selecteer en orden je de kaartlagen van de kaart.           | Per laag kunnen ook kaartspecifieke instellingen worden gedaan.     |
| **Thumbnail**                               | Hier kun je een thumbnail uploaden, wijzigen of verwijderen.     | De thumbnail kan optioneel worden gebruikt in de kaartomschrijving. |
| [**Kaartomschrijving**](#kaartomschrijving) | Hier stel je de inhoud van de informatiezijbalk van de kaart in. | Zie ook [Kaartomschrijving](#kaartomschrijving).                    |

### Beschikbare functies

| Functie                                      | Uitleg                                                              | Opmerking                                                                                                                                                                                                         |
| -------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Toon zoekbalk**                            | Toont de zoekbalk linksboven in de kaart.                           | Geen                                                                                                                                                                                                              |
| **Toon dataweergave**                        | Toont de dataweergave.                                              | Geen                                                                                                                                                                                                              |
| **Selecteer gebied**                         | Toont de functie om een gebied te selecteren.                       | Geen                                                                                                                                                                                                              |
| **Opmeten**                                  | Toont de meetfunctionaliteit.                                       | Geen                                                                                                                                                                                                              |
| **Meer opties**                              | Toont het menu met extra kaartopties.                               | Wordt automatisch ingeschakeld wanneer **Toon kaartomschrijving** wordt aangezet.                                                                                                                                 |
| **GPS knop**                                 | Toont de knop om de huidige locatie te gebruiken.                   | Geen                                                                                                                                                                                                              |
| **Zoomfunctie**                              | Toont de zoomknoppen.                                               | Geen                                                                                                                                                                                                              |
| **Toon schaal**                              | Toont de schaalaanduiding.                                          | Geen                                                                                                                                                                                                              |
| **Prikker bij klik**                         | Toont een prikker op de plek waar op de kaart is geklikt.           | Deze functionaliteit zorgt er ook voor dat er een detailweergave wordt getoond voor de aangeklikte plek.                                                                                                          |
| **Basislagen**                               | Toont de basislagenknop.                                            | Geen                                                                                                                                                                                                              |
| **Lagenlijst**                               | Toont de lagenlijst.                                                | Extra instellingen: **Verberg zoekbalk lagenlijst** en **Versimpelde weergave lagenlijst**.                                                                                                                       |
| **Legenda**                                  | Toont de legenda.                                                   | Geen                                                                                                                                                                                                              |
| **Lagenlijst en legenda standaard gesloten** | Opent de kaart met lagenlijst en legenda standaard ingeklapt.       | Geen                                                                                                                                                                                                              |
| **Lijstweergave**                            | Toont de lijstweergave.                                             | Kies een kaartlaag. Alleen lagen van type `WMS_WFS` zijn beschikbaar. Extra velden: **Template naam** en **Korte beschrijving**. In teksten kunnen kolomnamen uit de laag gebruikt worden met `{{ kolom_naam }}`. |
| **Filters**                                  | Toont de filterfunctionaliteit.                                     | Kies een kaartlaag. Alleen lagen van type `WMS_WFS` zijn beschikbaar. Selecteer vervolgens welke tekstvelden als filteroptie beschikbaar moeten zijn.                                                             |
| **Kaartlagen vergelijken**                   | Maakt de vergelijkfunctionaliteit voor kaartlagen beschikbaar.      | Geen                                                                                                                                                                                                              |
| **Tekenen**                                  | Maakt de tekenfunctionaliteit beschikbaar.                          | Geen                                                                                                                                                                                                              |
| **CRUD functionaliteit**                     | Maakt toevoegen, wijzigen en verwijderen van objecten mogelijk.     | Vereist aanvullende inrichting op kaartlaag- en autorisatieniveau. Zie ook [CRUD functionaliteit](crud_functionaliteit.md).                                                                                       |
| **Rondkijkfoto**                             | Toont de knop voor gekoppelde externe viewers voor rondkijkfoto's.  | Vereist geconfigureerde viewers.                                                                                                                                                                                  |
| **Herstelknop**                              | Toont een knop om terug te gaan naar de beginweergave van de kaart. | Geen                                                                                                                                                                                                              |

### Kaartomschrijving

Bij **Kaartomschrijving** configureer je de informatiezijbalk van de kaart.

| Veld                         | Uitleg                                                       | Opmerking                                                  |
| ---------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------- |
| **Toon kaartomschrijving**   | Toont een informatiezijbalk met extra context over de kaart. | Schakelt automatisch **Meer opties** in.                   |
| **Toon thumbnail in header** | Toont de geuploade thumbnail bovenaan de kaartomschrijving.  | Alleen beschikbaar als er eerst een thumbnail is geüpload. |
| **Toon 'Kaart delen' knop**  | Toont in de kaartomschrijving een knop om de kaart te delen. | Alleen relevant als de kaartomschrijving wordt getoond.    |
| **Header titel**             | De titel bovenaan de kaartomschrijving.                      | Optioneel.                                                 |
| **Zijbalk tekst**            | De inhoud van de kaartomschrijving.                          | Ondersteunt Markdown.                                      |

De kaartomschrijving is sluitbaar in de viewer en daarna opnieuw te openen via **Meer opties**.

### Lagen

Onder **Lagen** kies je welke kaartlagen in de kaart beschikbaar zijn. Je kunt hier ook de volgorde van lagen en hoofdcategorieën of subcategorieën bepalen. Per laag kan worden ingesteld of de standaardinstellingen van de kaartlaag worden overgenomen of dat de kaart een eigen laagconfiguratie gebruikt.

Meer informatie over kaartlagen staat in [kaartlagen](kaartlagen.md).

Kaartlagen kunnen daarnaast ook vanuit de kaartlaaginstellingen aan één of meerdere kaarten worden toegevoegd of daarvan worden verwijderd. Zie [Kaarten bij kaartlagen](kaartlagen.md#kaarten).

Klik op **Opslaan** om de gemaakte keuzes te bewaren.
