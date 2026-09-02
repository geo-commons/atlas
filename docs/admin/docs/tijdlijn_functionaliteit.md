# Tijdlijn

Met de tijdlijn kunnen gebruikers kaartlagen met tijdgegevens door de tijd bekijken. De tijdlijn toont een slider in de kaart waarmee een periode of peildatum gekozen kan worden. Atlas gebruikt hiervoor de WMS-T-standaard. De gekozen waarde wordt als `TIME` parameter meegestuurd naar de bron.

GeoServer ondersteunt WMS-T via tijdsdimensies op WMS-lagen. De tijdlijn werkt daarom alleen voor kaartlagen van type `WMS` of `WMS_WFS` waarbij de tijdsdimensie in GeoServer goed is geconfigureerd.

De tijdlijn werkt alleen wanneer deze op deze plek is ingericht:

- op de kaartlaag moet **Tijdlijn** zijn ingeschakeld

Zie ook [Kaartlagen](kaartlagen.md#tijdlijn).

## Configuratie GeoServer

Voor kaartlagen met tijdlijn moet de tijdsdimensie in GeoServer correct zijn ingesteld. Atlas geeft alleen de gekozen tijd of periode door aan de bron volgens de WMS-T-standaard. GeoServer bepaalt vervolgens welke objecten getoond moeten worden.

Configureer in GeoServer de tijdsdimensie op de laag die door Atlas wordt gebruikt. Welke Atlas instelling gebruikt kan worden hangt af van de dimensieconfiguratie in GeoServer:

| Configuratie GeoServer                  | Atlas configuratie                                                                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Alleen een startattribuut               | Gebruik de tijdlijn zonder **Peildatumweergave**. Peildatumweergave werkt in deze situatie niet.                                     |
| Een startattribuut en een eindattribuut | **Peildatumweergave** kan worden ingeschakeld. GeoServer kan dan bepalen welke objecten getoond moeten worden voor de gekozen datum. |

!!! warning "Let op"

    Schakel **Peildatumweergave** in Atlas alleen in wanneer in GeoServer zowel een startattribuut als een eindattribuut voor de tijdsdimensie is geconfigureerd. Wanneer GeoServer alleen een startattribuut heeft, werkt peildatumweergave niet goed.

## Werking in de kaart

De gebruiker kan in de kaart een tijdlijnlaag selecteren. Daarna verschijnt de slider onderin de kaart.

In het tijdlijnpaneel zijn de volgende opties beschikbaar:

| Optie            | Uitleg                                                                                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Kaartlaag**    | De tijdlijnlaag die met de slider wordt bediend. Alleen kaartlagen waarbij **Tijdlijn** is ingeschakeld zijn zichtbaar.                                              |
| **Weergave**     | Kies tussen **Periode** en **Peildatum**. Deze optie is alleen beschikbaar als **Peildatumweergave** op de kaartlaag is ingeschakeld.                                |
| **Sliderbereik** | De start- en einddatum waarbinnen de gebruiker de slider kan gebruiken. Deze datums kunnen worden aangepast binnen het bereik uit de OGC API collectie metadata. |
| **Stapgrootte**  | Bepaalt of de slider per **Dag**, **Maand** of **Jaar** verschuift.                                                                                                  |

Er kan maar één tijdlijnlaag tegelijk actief zijn. Wanneer een gebruiker een andere tijdlijnlaag inschakelt, wordt de vorige tijdlijnlaag uitgezet.

Op het moment dat de velden "Startdatumveld (GeoServer TIME)" en optioneel "Einddatumveld (GeoServer TIME)" op de tijdlijnlaag zijn ingesteld is de dataweergave ook in combinatie met de tijdlijnlaag bruikbaar. In de dataweergave worden dan de objecten getoond die actief zijn voor de gekozen periode of peildatum.

## Periode en peildatum

De tijdlijn kent twee manieren van werken:

| Weergave      | Uitleg                                                                                                                                        |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Periode**   | De gebruiker kiest een begin- en eindmoment. Atlas stuurt een periode naar GeoServer, bijvoorbeeld een volledig jaar, een maand of een dag.   |
| **Peildatum** | De gebruiker kiest één datum. GeoServer toont de objecten die geldig zijn op die datum. Dit vereist een start- en eindattribuut in GeoServer. |

Bij stapgrootte **Jaar** wordt de gekozen stap als volledig jaar gebruikt. Bij stapgrootte **Maand** wordt de volledige maand gebruikt. Bij stapgrootte **Dag** wordt de gekozen dag gebruikt.

## Bereik

Atlas bepaalt het beschikbare tijdslider bereik automatisch op basis van de metadata van de geselecteerde laag. Deze automatische bepaling wordt alleen ondersteund voor GeoServer-bronnen, omdat Atlas hiervoor de `extent.temporal.interval` uit de GeoServer OGC API collectie gebruikt.

Atlas leidt het OGC API collection endpoint af van de OWS-bron van de kaartlaag. Daarbij wordt dezelfde host gebruikt als in de OWS-url. Voor niet-geauthenticeerde bronnen vraagt Atlas de collectie op via `/geoserver/ogc/maps/v1/collections/{laagnaam}`. Voor geauthenticeerde bronnen loopt dit via filter-proxy: `/api/ogc/maps/v1/collections/{laagnaam}`. De `{laagnaam}` is de naam van de kaartlaag zoals die in Atlas is ingesteld.

De minimale datum uit de metadata is de minimale waarde van de startdatum. De maximale datum uit de metadata is de maximale waarde van de einddatum. Binnen deze grenzen kan de gebruiker het actieve sliderbereik aanpassen.

!!! info

    Wanneer de metadata geen bruikbaar tijdbereik bevat, blijft de laag selecteerbaar maar toont Atlas een foutmelding in het tijdlijnpaneel. Er wordt dan geen `TIME` parameter meegestuurd naar de bron.
