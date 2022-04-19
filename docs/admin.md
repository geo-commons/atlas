# Handleiding Admin Module Atlas versie 3.8.5

## Deze handleiding beschrijft de werking van de Admin Module. In de Admin Module wordt Atlas geconfigureerd.

#### LET OP: (*) Deze opties zijn bij het maken van deze handleiding nog niet functioneel (06-04-2022)

### Inhoud

* [INTRODUCTIE](#introductie)
* [HOOFDSCHERM](#hoofdscherm)
* [CONFIGURATIE](#configuratie)
* [GEBRUIKERSBEHEER](#gebruikersbeheer)
     * [Groepen](#groepen)
* [KAARTEN](#kaarten)
     * [Categorieën](#categorieën)
     * [Kaartlagen](#kaartlagen)
     * [Kaarten](#kaarten)
* [HOMEPAGE](#homepage)
     * [Saved_datasets](#saved_datasets)
#### INTRODUCTIE

Bij het installeren van Atlas wordt in de laatste stap een superuser aangemaakt. In de README.MD file is dit beschreven.  Met deze gebruiker (superuser) kan in de adminmodule worden ingelogd op http://localhost:8000/atlas/admin/ . Let op dat de url eindigt met een /.  
Binnen de adminmodule kunnen additionele gebruikers worden aangemaakt en rechten worden toegekend. Alleen gebruikers met supergebruikerstatus hebben toegang tot de adminmodule.  
Via de parameter CTRIX_IPS (zie README.md) kan worden bepaald welke ip adressen toegang hebben tot de adminmodule. Om beveiligingsredenen zouden deze ip adressen altijd binnen het netwerk van de interne WFS server moeten liggen.  
Het inloggen in de adminmodule verloopt via Single-Sign-On. Het openen van de adminmodule buiten het interne netwerk leidt tot een foutmelding
<img src="/uploads/f576c11e29eed968c24000ba110e9786/inlog-admin-sso.png" alt="Inlogscherm Adminmodule" width="300"/>



***
* [Naar boven](#inhoud)
***

#### HOOFDSCHERM

Het hoofdscherm **Websitebeheer** laat een aantal onderdelen zien die ingesteld kunnen worden.

<img src="/uploads/aa975c1f520d44e7ecbf35ecae0751d5/hoofdmenu.png" alt="Hoofdscherm Admin module" width="500"/>


***
* [Naar boven](#inhoud)
***

#### CONFIGURATIE
Hier kunnen de globale instellingen gedaan worden die in Atlas getoond worden.  
Config. 

1. Organisatie

ORGANIZATION_NAME   De naam van de organisatie die getoond moet worden.  
FAVICON_URL         Het icoon dat in de tabbalk van de browser zichtbaar wordt.  
DISCLAIMER          Mogelijke voorwaardelijkheidsverklaring. Als deze niet is ingevuld is de optie ook niet aanwezig in het Atlasscherm.

2. Kaartconfiguratie  

POSITION_CENTER_X        Het centrum X-coördinaat van de opstartpositie.  
POSITION_CENTER_Y        Het centrum Y-coördinaat van de opstartpositie.  
POSITION_ZOOM            Het zoomniveau van de opstartpositie.  
SUGGEST_MUNICIPALITIES   Een komma-gescheiden lijst van gemeenten om adressen in te zoeken (voor auto-aanvulfunctionaliteit).  

***
* [Naar boven](#inhoud)
***

##### GEBRUIKERSBEHEER
In het gebruikersbeheerscherm bevindt zich het aanmaken en bewerken van Atlas gebruikers. Atlas gebruikers kunnen op hun beurt weer toegevoegd worden aan een Atlas groep.   
(*) Groepen kunnen aangemaakt worden om toegang tot lagen te configureren. 


In het gebruikersscherm kan een gebruiker worden toegevoegd of bewerkt. Voor een nieuwe gebruiker moet een gebruikersnaam en wachtwoord worden ingegeven. De gebruikersnaam moet 150 tekens of minder lang zijn. Alleen letters, cijfers en @/,/+/-/_ tekens zijn toegestaan. Aan het wachtwoord zijn de volgende beperkingen gebonden: 
* Uw wachtwoord mag niet te veel lijken op uw overige persoonlijke informatie. 
* Uw wachtwoord moet minstens 8 tekens lang zijn. 
* Uw wachtwoord mag geen veelgebruikt wachtwoord zijn. 
* Uw wachtwoord mag niet volledig uit cijfers bestaan.

Klik op Opslaan om deze gegevens naar de database te schrijven. Nu verschijnt een uitgebreid scherm waarin extra gebruikergegevens kunnen worden ingegeven of gewijzigd. Wanneer er ook groepen zijn aangemaakt, kan hier de gebruiker aan een of meerdere groepen worden toegevoegd. Houd 'Control', of 'Command' op een Mac, ingedrukt om meerdere items te selecteren.

<img src="/uploads/d228a44b188e28689c405b9a185cff9b/gebruiker-toevoegen.png" alt="gebruiker toevoegen" width="1400"/>

In het Gebruiker Wijzigen scherm kan uitgebreide gebruikersinformatie worden toegevoegd of gegevens gewijzigd.

<img src="/uploads/7307bf8f38c0d8794bf9e425e4640c71/_gebruikerswijzigen2.png" alt="gebruiker wijzigen 2" width="1400"/>

***
* [Naar boven](#inhoud)
***

##### Groepen
In het Atlas Groep Toevoegen scherm kunnen groepen worden aangemaakt. Wanneer er ook gebruikers zijn aangemaakt kunnen deze hier aan de groep worden toegvoegd.

<img src="/uploads/4c3cb144ebbf90680b36214e215a4128/atlas-groep-toevoegen.png" alt="atlas groep toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***

#### KAARTEN

Binnen kaarten kunnen Bronnen, Categorieën, Kaarten, Kaartlagen en Viewers worden toegevoegd. De optie Thema's is vervangen door Kaarten en komt te vervallen.
* Bronnen bevat mogelijke URL's vanwaar de kaartlagen geserveerd worden.
* Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond. (*) Daarnaast kunnen Categorieën als tegel op het hoofdscherm weergegeven worden.
Het aanmaken en toekennen van categorieën helpt bij het geordend houden van de legenda.
* Kaartlagen zijn de datasets die binnen Atlas ontsloten worden.
Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere kaarten.
* Kaarten zijn verzamelde kaartlagen die samen over een bepaald onderwerp gaan.
Bij het aanmaken van een kaart wordt een nieuwe url gecreëerd, waar een aparte instantie van Atlas wordt getoond met een beperkter aantal kaartlagen en beperktere functionaliteit.
* Viewers bevat de externe applicaties die worden gebruikt voor rondkijkfoto's (bijv. Google Maps)

***
* [Naar boven](#inhoud)
***

##### Categorieën
Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond. Het openklikken van een hoofdonderwerp/categorie
zorgt ervoor dat eronder de verschillende kaartlagen van die categorie in de legenda worden getoond.
Bij het toevoegen van een kaartlaag wordt aangegeven onder welke categorie deze valt. 
(*) Er kan voor gekozen worden om een categorie als tegel op het hoofdscherm weer te geven of alleen in de lijstweergave of beide.

<img src="/uploads/d4c30aacd2dc65073eb3c39881516990/categorieen.png" alt="categorieën" width="400"/>

De volgende velden moeten worden ingevuld bij het toevoegen van een categorie:
* **Titel:** (De naam zoals die in het viewer scherm van Atlas komt te staan)
* **Sortering:** (default waarde: 0)

 
<img src="/uploads/2c695502d3e2ad833349e805601b6a00/categorie-toevoegen.png" alt="categorie toevoegen" width="500"/>


***
* [Naar boven](#inhoud)
***

##### Kaartlagen
Kaartlagen zijn de datasets die binnen Atlas ontsloten worden. 
Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere kaarten. 

Bij het aanmaken van een nieuwe kaartlaag kan gekozen worden om een nieuwe kaartlaag toe te voegen of een bestaande te bewerken en deze als nieuwe kaartlaag op te slaan. Dit kan handig zijn als niet alle gegevens opnieuw ingevoerd te hoeven worden.


De volgende velden moeten worden ingevuld bij het toevoegen van een kaartlaag:
* **Titel:** (De naam zoals die verschijnt in de legenda van Atlas. De invoer mag geen 'speciale' tekens bevatten)
* **Kort kenmerk:** (Een uniek ID dat de layer onderscheid van andere. 
* **Categorie:** (selecteer onder welke categorie deze layer komt)
* **Gepubliceerd:** (wordt de laag gepubliceerd of niet. deze optie kan gebruikt worden om de laag tijdens het configureren nog niet aan Atlas aan te bieden, of om deze snel (tijdelijk) uit Atlas te verwijderen zonder dat de volledige kaartlaagconfiguratie verwijderd hoeft te worden.)(Default: uit)  

* **Bron:** (Selecteer er één zoals die bij 'Bronnen' zijn geconfigureerd). 
* **Laagnaam:** (De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bv: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver.)
* **Brontype:** (Selecteer het type voor deze laag)
* **Projectie:** (De projectie waarin de kaartlaag bevraagd wordt. Default: EPSG:28992)
* **Server type:** (standaard: geoserver)  

* **Transparantie:** (default 0,9)

* **Meta_naam:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Adressen(BAG))
* **Meta_soort:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Basisregistratie)
* **Meta_org:** ([Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Geoinformatie
* **Meta_bijgewerkt:** (De waarde wordt door Javascript geëvalueerd (Bijv:"01-01-2018",getDate("year"). Default: getDate("full"))
* **Is basislaag:** (Aanzetten als de laag als achtergrondlaag moet dienen)
* **Is standaard zichtbaar:** (Eigenlijk zelfde als hierboven maar komt bovenop de basislaag)
* **Toon laag alleen in een themakaart:** (Kaartlaag wordt niet in Atlas getoond, alleen als kaartlaag in de kaarten waaraan deze is toegevoegd. Wanneer deze optie niet is aangevinkt is de laag zowel in een kaart als in het hoofdscherm zichtbaar)
* **Kan doorzocht worden:** (maak het mogelijk de laag te bevragen door in de kaart te klikken (popup attriutes) én maak de layer zichtbaar in de zoekfunctie )
* **Toon deze velden:** ([Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in dit pop-up venster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond.)
* **Doorzoek deze velden:** (Selecteer de velden waar bij Zoeken op Data op gezocht kan worden. Als dit leeg gelaten wordt, worden alle attributen zoekvelden.)
* **Bereik minimum x:** (Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt)
* **Bereik minimum y:** (Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt)
* **Bereik maximum x:** (Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt)
* **Bereik maximum y:** (Vul in om de laag inactief te maken wanneer de weergave buiten het bereik ligt)
* **Zoomniveau minimum:** (Vul in om de laag inactief te maken wanneer de weergave buiten het zoomniveau ligt)
* **Zoomniveau maximum:** (Vul in om de laag inactief te maken wanneer de weergave buiten het zoomniveau ligt)
* **Stijl:** (Voeg een stijlbestand in Geostyler formaat toe. Hiermee wordt de WFS stijl in Geoserver overruled)
* **Naam:** (Vul een naam in voor de laag als metadata. Deze informatie verschijnt wanneer op het 'i' symbool wordt geklikt)
* **Soort:** (Vul een categorie in voor de laag als metadata. Deze informatie verschijnt wanneer op het 'i' symbool wordt geklikt)
* **Organisatie:** (Vul de eigenaar van de betreffende data in. Deze informatie verschijnt wanneer op het 'i' symbool wordt geklikt)
* **Laatst bijgewerkt:** (Datum laatst bijgewerkt. Deze informatie verschijnt wanneer op het 'i' symbool wordt geklikt)
* **Alleen intern zichtbaar:** (is de kaartlaag ook buiten het interne netwerk zichtbaar)
* **Vereis inlog voor deze dataset:** (Wanneer deze optie is aangevinkt, dan verschijnt de laag met een slotje ten teken dat men moet inloggen om de laag te zien)


* **Eigenaar:** (Wie is eigenaar van deze layer)   
* **Gebruikers:** (Welke gebruikers hebben toegang tot deze kaartlaag?   
* **Groepen:** (Welke Atlas gebruikersgroepen hebben toegang tot deze kaartlaag? )
* **Gekoppelde Data:** (...)



***
* [Naar boven](#inhoud)
***

##### Kaarten
Kaarten zijn verzamelingen kaartlagen die samen over een bepaald onderwerp gaan. Om een kaart samen te stellen worden kaartlagen geselecteerd die bij die kaart horen.  
Een kaart verschijnt niet in het Atlas scherm. Bij het aanmaken van een kaart wordt als het ware een aparte instantie van Atlas gecreëerd met een beperkter aantal kaartlagen en beperktere functionaliteit. Wanneer bijvoorbeeld een kaart 'hondenbeleid' is aangemaakt waarin de kaartlagen 'hondenuitlaatplekken' en  'hondenbakken' zitten, dan kan de url om de kaart op te vragen er bijvoorbeeld zo uitzien: https://mijngemeentewebsite.nl/atlas/hondenbeleid

<img src="/uploads/0ac41b64d0d39964456faccfb95e744a/hondenbeleid.png" alt="hondenbeleid" width="500"/>



De volgende velden moeten worden ingevuld bij het toevoegen van een kaart:
* **Title:** ([De naam zoals die ook bij de url ingegeven moet worden)
* **Layers:** (De layers die binnen het Thema vallen)
Houd 'Control', of 'Command' op een Mac, ingedrukt om meerdere kaartlagen te selecteren.

<img src="/uploads/de986950d607214fb299ead6ddceea15/thema-toevoegen.png" alt="Thema Toevoegen" width="700"/>

***
* [Naar boven](#inhoud)
***

#### HOMEPAGE

##### Saved_datasets

Binnen Atlas bestaat de mogelijkheid om adressen binnen een kaart te selecteren. Dit kan door middel van de CTRL toets ingedrukt te houden en tegelijkertijd met de muis een gebied met adressen te selecteren. Ook kunnen adressen geselecteerd worden met behulp van de selectietool rechtsboven in het Atlas scherm. Deze adres-selecties worden op het scherm getoond maar kunnen ook gedownload worden. Binnen Atlas zelf worden deze selecties in de database opgeslagen. Via de "Saved Datasets" optie, kunnen deze selecties beheerd worden.

<img src="/uploads/6e24a14bced7de4e249788295521bad8/saved-datasets.png" alt="Saved datasets" width="600"/>

Wanneer een "saved dataset" wordt geselecteerd, dan zal de inhoud in het JSON scherm getoond worden.

<img src="/uploads/37b1076c9dd8a046eefa55a6bfb42453/saved-dataset-wijzigen.png" alt="Saved dataset wijzigen" width="600"/>

Ook is het mogelijk om via cut & paste zelf datasets toe te voegen voor eventueel toekomstig gebruik.

<img src="/uploads/1c5b79fa7cac606e932504428185c628/dataset-toevoegen.png" alt="Dataset toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***













