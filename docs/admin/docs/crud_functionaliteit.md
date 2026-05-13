# Objecten muteren in Atlas via de kaartinterface

In Atlas is het mogelijk om direct vanuit de kaartinterface objecten op een kaartlaag te muteren (toevoegen, bewerken en verwijderen) als ingelogde gebruiker, wanneer de juiste zaken zijn ingesteld. In dit document wordt uitgelegd hoe je deze functionaliteit kunt configureren en gebruiken.

## 1. GeoServer-configuratie

Voordat je objecten op een kaartlaag kunt muteren, moet GeoServer correct geconfigureerd zijn. Op kaartlaag-niveau kun je in GeoServer toegangsrechten toewijzen aan gebruikers.

Om mutaties mogelijk te maken, is het essentieel dat de gebruiker **FILTER_PROXY** schrijfrechten heeft op de betreffende kaartlaag. In dit [artikel](layer_security.md) wordt uitgelegd hoe je dit instelt.

## 2. Atlas-configuratie

> ⚠️ **Let op:** De mutatiefunctie werkt alleen met kaartlagen die worden geraadpleegd via **filter-proxy** (of de naam die deze bron bij jullie binnen GeoServer heeft).

### 2.1 Activeren op kaartniveau

De CRUD-functionaliteit (Create, Read, Update, Delete) is alleen beschikbaar als de optie **CRUD-functionaliteit** is ingeschakeld in de configuratie van de kaart waarvoor bewerken gewenst is.

### 2.2 Configuratie op kaartlaagniveau

Op kaartlaagniveau moeten toegangsregels worden ingesteld om de mutatiefunctie te kunnen gebruiken. Hoe je dit instelt, lees je in [deze handleiding](kaartlagen.md/#toegang). Daarnaast is het van belang om te weten dat de kaartlaag naam altijd de GeoServer omgeving in de naam moet hebben op het moment dat je CRUD functionaliteit wil gebruiken. Zo wordt bijvoorbeeld een kaartlaag met naam "scholen" "topp:scholen" als de GeoServer omgeving de topp omgeving is.

### 2.3 Configuratie via autorisaties

Als je geen toegangsregels op kaartlaagniveau wilt instellen, kun je de CRUD-functionaliteit ook beschikbaar maken via toegangsregels in een gekoppelde **autorisatieregel**. Meer informatie hierover vind je [hier](autorisaties.md/#toegang).

### 2.4 Samenvatting

| Stap | Actie                                                                               |
| ---- | ----------------------------------------------------------------------------------- |
| 1    | Zorg dat de gebruiker **FILTER_PROXY** schrijfrechten heeft in GeoServer.           |
| 2    | Zet de feature flag **"Bewerkfunctionaliteit"** aan in de admin-omgeving van Atlas. |
| 3    | Gebruik een kaartlaag met **filter-proxy** als gegevensbron.                        |
| 4    | Stel toegangsregel                                                                  |

## 3. Het gebruik van de CRUD-functionaliteit

Dit onderdeel beschrijft het gebruik van de CRUD-functionaliteit in Atlas. Dit is alleen beschikbaar voor ingelogde gebruikers en alleen als de configuratie correct is ingesteld voor de bijbehorende kaartlaag.

### 3.1 De interface

Zodra de configuratie goed is ingesteld, verschijnt er in de kaartinterface van Atlas een extra knop:

![Knop CRUD-functionaliteit](../images/knop_crud_functionaliteit.png)

> 📌 **Let op:** Zorg ervoor dat de kaartlaag waarop je wilt muteren **actief** is. Dit doe je zoals gebruikelijk via het lagenpaneel.

Zodra de gewenste laag actief is, kun je op de knop drukken. Dan verschijnt het volgende scherm:

![Object toevoegen of bewerken](../images/object_toevoegen_knop.png)

- Klik op het **plus-icoon** om een object toe te voegen.

### 3.2 Een object toevoegen

Wanneer je op het **plus-icoon** klikt, kun je direct een object op de kaart tekenen. Atlas bepaalt automatisch het type geometrie op basis van de geselecteerde kaartlaag.

#### Toevoegen: Point, Polygon, LineString, LinearRing of Circle

1. Teken het gewenste object op de kaart.
2. Rond de tekening af door op **Enter** te drukken of te dubbelklikken.

#### Toevoegen: MultiPoint, MultiPolygon of MultiLineString

1. Teken de gewenste objecten op de kaart. Gebruik een dubbelklik om één onderdeel van het multi-object af te ronden. Herhaal dit proces om meerdere onderdelen toe te voegen aan hetzelfde object.
2. Rond de volledige tekening af door op **Enter** te drukken.

#### Afronden en opslaan (geldt voor alle objecttypen)

1. Er opent automatisch een invoerpaneel aan de linkerzijde op desktop en aan de onderzijde op mobiel/tablet.

   ![Object toevoegen paneel](../images/toevoeg_paneel_crud.png)

2. In dit paneel worden automatisch de velden getoond die bij de laag horen. Vul de relevante gegevens in.
3. Klik op **Opslaan** om het object op te slaan.

> ✅ De mutatie wordt uitgevoerd op de GeoServer en opgeslagen in de gekoppelde datastore.

### 3.3 Een object bewerken of verwijderen

Je kunt een object op deze manier bewerken of verwijderen:

**Via de detailweergave**:

- Klik het object aan.
- Druk op de knop **"Bewerk"** in de detailweergave.

Hierna opent zich het volgende paneel:

![Object bewerken paneel](../images/bewerk_paneel_crud.png)

In dit paneel kun je:

- Gegevens van het object aanpassen
- Het opject opnieuw tekenen door op **"Opnieuw tekenen"** te klikken.
- Het object volledig verwijderen door op **"Verwijderen"** te klikken.
- Wijzigingen opslaan door op **"Opslaan"** te klikken.

Ook kan je in de kaart de geometrie van het object bewerken, door het object te selecteren en punt(en) van het object te slepen naar de gewenste locatie.

> 🔁 Alle bewerkingen en verwijderingen worden direct doorgevoerd in GeoServer en de gekoppelde datastore.
