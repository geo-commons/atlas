# Objecten muteren in Atlas via de kaartinterface

In Atlas is het mogelijk om direct vanuit de kaartinterface objecten op een kaartlaag te muteren (toevoegen, bewerken en verwijderen) als ingelogde gebruiker, wanneer de juiste zaken zijn ingesteld. In dit document wordt uitgelegd hoe je deze functionaliteit kunt configureren en gebruiken.

## 1. GeoServer-configuratie

Voordat je objecten op een kaartlaag kunt muteren, moet GeoServer correct geconfigureerd zijn. Op kaartlaag-niveau kun je in GeoServer toegangsrechten toewijzen aan gebruikers.

Om mutaties mogelijk te maken, is het essentieel dat de gebruiker **FILTER_PROXY** schrijfrechten heeft op de betreffende kaartlaag. In dit [artikel](/layer_security) wordt uitgelegd hoe je dit instelt.

## 2. Atlas-configuratie

> ⚠️ **Let op:** De mutatiefunctie werkt alleen met kaartlagen die worden geraadpleegd via **filter-proxy** (of de naam die deze bron bij jullie binnen GeoServer heeft).

### 2.1 Feature flag activeren

De CRUD-functionaliteit (Create, Read, Update, Delete) is alleen beschikbaar als je in de **Configuratie module** binnen de admin-omgeving de feature flag **"Bewerkfunctionaliteit"** hebt ingeschakeld.

### 2.2 Configuratie op kaartlaagniveau

Op kaartlaagniveau moeten toegangsregels worden ingesteld om de mutatiefunctie te kunnen gebruiken. Hoe je dit instelt, lees je in [deze handleiding](/kaartlagen/#toegang). Daarnaast is het van belang om te weten dat de kaartlaag naam altijd de GeoServer omgeving in de naam moet hebben op het moment dat je CRUD functionaliteit wil gebruiken. Zo wordt bijvoorbeeld een kaartlaag met naam "scholen" "topp:scholen" als de GeoServer omgeving de topp omgeving is.

### 2.3 Configuratie via autorisaties

Als je geen toegangsregels op kaartlaagniveau wilt instellen, kun je de CRUD-functionaliteit ook beschikbaar maken via toegangsregels in een gekoppelde **autorisatieregel**. Meer informatie hierover vind je [hier](/autorisaties/#toegang).

### 2.4 Samenvatting

| Stap | Actie                                                                                   |
|------|------------------------------------------------------------------------------------------|
| 1    | Zorg dat de gebruiker **FILTER_PROXY** schrijfrechten heeft in GeoServer.               |
| 2    | Zet de feature flag **"Bewerkfunctionaliteit"** aan in de admin-omgeving van Atlas.     |
| 3    | Gebruik een kaartlaag met **filter-proxy** als gegevensbron.                            |
| 4    | Stel toegangsregel

## 3. Het gebruik van de CRUD-functionaliteit

Dit onderdeel beschrijft het gebruik van de CRUD-functionaliteit in Atlas. Dit is alleen beschikbaar voor ingelogde gebruikers en alleen als de configuratie correct is ingesteld voor de bijbehorende kaartlaag.

### 3.1 De interface

Zodra de configuratie goed is ingesteld, verschijnt er in de kaartinterface van Atlas een extra knop:

![Knop CRUD-functionaliteit](../images/knop_crud_functionaliteit.png)

> 📌 **Let op:** Zorg ervoor dat de kaartlaag waarop je wilt muteren **actief** is. Dit doe je zoals gebruikelijk via het lagenpaneel.

Zodra de gewenste laag actief is, kun je op de knop drukken. Dan verschijnt het volgende scherm:

![Object toevoegen of bewerken](../images/object_toevoegen_knop.png)

- Klik op het **plus-icoon** om een object toe te voegen.
- Klik op het **pen-icoon** om een bestaand object te bewerken.

### 3.2 Een object toevoegen

Wanneer je op het **plus-icoon** klikt, krijg je direct de mogelijkheid om een object op de kaart te tekenen. Atlas bepaalt automatisch of het hierbij gaat om een punt, lijn of polygoon – afhankelijk van het type kaartlaag.

1. Teken het gewenste object op de kaart.
2. Rond de tekening af door op **Enter** of dubbel te klikken.
3. Er opent zich nu een invoerpaneel aan de linkerzijde (desktop) of onderzijde (mobiel/tablet):

![Object toevoegen paneel](../images/toevoeg_paneel_crud.png)

4. In dit paneel zie je automatisch de velden die bij de laag horen. Vul de relevante gegevens in.
5. Klik op **Opslaan** om het object op te slaan.

> ✅ De mutatie wordt uitgevoerd op de GeoServer en opgeslagen in de gekoppelde datastore.

### 3.3 Een object bewerken of verwijderen

Je kunt een object op twee manieren bewerken of verwijderen:

1. **Via de detailweergave**:
   - Klik het object aan.
   - Druk op de knop **"Bewerk"** in de detailweergave.

2. **Via het pen-icoon**:
   - Activeer het pen-icoon.
   - Klik op het object dat je wilt aanpassen.

Hierna opent zich het volgende paneel:

![Object bewerken paneel](../images/bewerk_paneel_crud.png)

In dit paneel kun je:

- Gegevens van het object aanpassen.
- Wijzigingen opslaan door op **"Opslaan"** te klikken.
- Het object volledig verwijderen door op **"Verwijderen"** te klikken.

> 🔁 Alle bewerkingen en verwijderingen worden direct doorgevoerd in GeoServer en de gekoppelde datastore.

