# Handleiding Admin Module Atlas versie 2.2.4

## Deze handleiding beschrijft de werking van de Admin Module. In de Admin Module wordt Atlas geconfigureerd.

### Inhoud

* [INTRODUCTIE](#introductie)
* [HOOFDSCHERM](#hoofdscherm)
* [USER_MANAGEMENT](#user_management)
     * [Gebruikers](#gebruikers)
     * [Atlas_groups](#atlas_groups)
* [WEBSERVICE](#webservice)
     * [Categorieën](#categorieën)
     * [Kaartlagen](#kaartlagen)
     * [Kaarten](#kaarten)
* [HOMEPAGE](#homepage)
     * [Saved_datasets](#saved_datasets)
* [AUTHENTICATIE EN AUTORISATIE](#authenticatie-en-autorisatie)
     * [Groepen](#groepen)
#### INTRODUCTIE

Bij het installeren van Atlas wordt in de laatste stap een superuser aangemaakt. In de README.MD file is dit beschreven.  Met deze gebruiker (superuser) kan in de adminmodule worden ingelogd op http://localhost:8000/atlas/admin/ .


Let op dat de url eindigt met een /.

***
* [Naar boven](#inhoud)
***

#### HOOFDSCHERM

Het hoofdscherm **Websitebeheer** laat een aantal onderdelen zien die ingesteld kunnen worden.

<img src="/uploads/7478bfaf4c2986cecdd3f3bb819f60db/hoofdscherm.png" alt="Hoofdscherm Admin module" width="1000"/>


***
* [Naar boven](#inhoud)
***

#### USER_MANAGEMENT
In user management bevindt zich het aanmaken en bewerken van Atlas gebruikers. Atlas gebruikers kunnen op hun beurt weer toegevoegd worden
aan een Atlas group. Het gebruikersbeheer heeft geen relatie met groepen in authenticatie en autorisatie.


##### Gebruikers
Klik in het user management beheer scherm bij gebruikers op Toevoegen om een gebruiker toe te voegen.

<img src="/uploads/1b8d33f8a57599b0381758859a5c4138/user-magement-beheer.png" alt="Gebruikersbeheer" width="600"/>

In het volgende scherm kan een gebruikersnaam en wachtwoord worden ingegeven. De gebruikersnaam moet 150 tekens of minder lang zijn. Alleen letters, cijfers en @/,/+/-/_ tekens zijn toegestaan. Aan het wachtwoord zijn de volgende beperkingen gebonden: 
* Uw wachtwoord mag niet te veel lijken op uw overige persoonlijke informatie. 
* Uw wachtwoord moet minstens 8 tekens lang zijn. 
* Uw wachtwoord mag geen veelgebruikt wachtwoord zijn. 
* Uw wachtwoord mag niet volledig uit cijfers bestaan.

Klik op Opslaan om deze gegevens naar de database te schrijven. Nu verschijnt een uitgebreid scherm waarin extra gebruikergegevens kunnen worden ingegeven of gewijzigd. Wanneer er ook groepen zijn aangemaakt, kan hier de gebruiker aan een of meerdere groepen worden toegevoegd. Houd 'Control', of 'Command' op een Mac, ingedrukt om meerdere items te selecteren.

<img src="/uploads/d228a44b188e28689c405b9a185cff9b/gebruiker-toevoegen.png" alt="gebruiker toevoegen" width="1400"/>

In het Gebruiker Wijzigen scherm kan uitgebreide gebruikersinformatie worden toegevoegd of gegevens gewijzigd.

<img src="/uploads/7307bf8f38c0d8794bf9e425e4640c71/_gebruikerswijzigen2.png" alt="gebruiker wijzigen 2" width="1400"/>


##### Atlas_groups
In het Atlas Groep Toevoegen scherm kunnen groepen worden aangemaakt. Wanneer er ook gebruikers zijn aangemaakt kunnen deze hier aan de groep worden toegvoegd.

<img src="/uploads/4c3cb144ebbf90680b36214e215a4128/atlas-groep-toevoegen.png" alt="atlas groep toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***

#### WEBSERVICE

<img src="/uploads/a8d17641ad4383eff163ec9121619711/webservice-beheer.png" alt="Webservice beheer" width="600"/>

Binnen webservice kunnen Categorieën, kaartlagen en kaarten worden toegevoegd.
* Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond.
Het aanmaken en toekennen van categorieën helpt bij het geordend houden van de legenda.
* Kaartlagen zijn de datasets die binnen Atlas ontsloten worden.
Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere kaarten.
* Kaarten zijn verzamelde kaartlagen die samen over een bepaald onderwerp gaan.
Bij het aanmaken van een kaart wordt een nieuwe url gecreëerd, waar een aparte instantie van Atlas wordt getoond met een beperkter aantal kaartlagen en beperktere functionaliteit.

##### Categorieën
Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond. Het openklikken van een hoofdonderwerp/categorie
zorgt ervoor dat eronder de verschillende kaartlagen van die categorie in de legenda worden getoond.
Bij het toevoegen van een kaartlaag wordt aangegeven onder welke categorie deze valt.
Categorieën worden getoond op alfabetische volgorde, onder Achtergrondkaarten en Luchtfoto's. Hou hier rekening mee bij het aanmaken van een categorie.

<img src="/uploads/32f72073d636bb6178f0da5ec3a47ea2/categorieenkopie.png" alt="categorieën" width="500"/>

De volgende velden moeten worden ingevuld bij het toevoegen van een categorie:
* **Title:** (De naam zoals die in het viewer scherm van Atlas komt te staan, denk hierbij om de alfabetische volgorde)
* **Javascript type:** (default waarde: themelayer:true)
* **Gesloten thema** (Is deze categorie in alle omgevingen zichtbaar of alleen intern?)
 
<img src="/uploads/da7708c048d82f68c69ed0e062651027/categorie-toevoegen.png" alt="categorie toevoegen" width="500"/>


***
* [Naar boven](#inhoud)
***

##### Kaartlagen
Kaartlagen zijn de datasets die binnen Atlas ontsloten worden. 
Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere thema's. 

<img src="/uploads/e3ffddfcbfe4dc3573a07816a9c55b36/kaartlagenkopie.png" alt="kaartlagen" width="500"/>


De volgende velden moeten worden ingevuld bij het toevoegen van een kaartlaag:
* **Layer_id:** (Een uniek ID dat de layer onderscheid van andere. De invoer mag geen verbindingsstreepje - bevatten) 
* **Title:** (De naam zoals die verschijnt in de legenda van Atlas. De invoer mag geen 'speciale' tekens bevatten)
* **Layer_name:** (De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bv: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver.)
* **Meta_naam:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Adressen(BAG))
* **Meta_soort:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Basisregistratie)
* **Meta_org:** ([Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Geoinformatie
* **Meta_bijgewerkt:** (De waarde wordt door Javascript geëvalueerd (Bijv:"01-01-2018",getDate("year"). Default: getDate("full"))
* **Opacity:** (default 0,9)
* **Visible:** (is deze layer zichtbaar in de viewer?)
* **Categorie:** (selecteer onder welke categorie deze layer komt)
* **ISqueryable:** (maak het mogelijk de laag te bevragen door in de kaart te klikken (popup attriutes) én maak de layer zichtbaar in de zoekfunctie )
* **Popup attributes:** ([Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in dit pop-up venster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond.)
* **Search fields:** (Selecteer de velden waar bij Zoeken op Data op gezocht kan worden. Als dit leeg gelaten wordt, worden alle attributen zoekvelden.)
* **Projection:** (De projectie waarin de kaartlaag bevraagd wordt. Default: EPSG:28992)
* **Url:** De URL van de layer (http://GEOSERVER_URL/wms?...) Het gebruikte endpoint (zie ook de <a href="https://docs.geoserver.org/stable/en/user/geowebcache/webadmin/defaults.html#gwc-webadmin-defaults">Geoserver handleiding</a>)
* **Server type:** (standaard: geoserver)
* **Gesloten data:** (is de layer ook buiten het interne netwerk zichtbaar)
* **Gepubliceerd:** (wordt de laag gepubliceerd of niet. deze optie kan gebruikt worden om de laag tijdens het configureren nog niet aan Atlas aan te bieden, of om deze snel (tijdelijk) uit Atlas te verwijderen zonder dat de volledige kaartlaagconfiguratie verwijderd hoeft te worden.)(Default: aan)
* **Alleen in een thema, niet in Atlas:** (Kaartlaag wordt niet in Atlas getoond, alleen als kaartlaag in de thema's waaraan deze is toegevoegd)
* **Owner:** (Wie is eigenaar van deze layer) 
* **Users:** (Welke gebruikers hebben toegang tot deze kaartlaag? 
* **Atlas groups:** (Welke Atlas gebruikersgroepen hebben toegang tot deze kaartlaag? )
* **Ordening:** (uniek nummer dat de rangschikking binnen het viewer scherm bepaalt. Let op: dit nummer moet uniek zijn, anders zullen de lagen binnen Atlas niet laden)

<img src="/uploads/98dd32f3456b99db5bd98525f6122b19/kaartlaag-toevoegen.png" alt="kaartlaag toevoegen" width="700"/>

***
* [Naar boven](#inhoud)
***

##### Kaarten
Kaarten zijn verzamelingen kaartlagen die samen over een bepaald onderwerp gaan. Om van een kaarten samen te stellen worden kaartlagen geselecteerd die bij die kaart horen. 

Een kaart verschijnt niet in het Atlas scherm. Bij het aanmaken van een kaart wordt als het ware een aparte instantie van Atlas gecreëerd met een beperkter aantal kaartlagen en beperktere functionaliteit. Wanneer bijvoorbeeld een kaart 'hondenbeleid' is aangemaakt waarin de kaartlagen 'hondenuitlaatplekken' en  'hondenbakken' zitten, dan kan de url om de kaart op te vragen er bijvoorbeeld zo uitzien: https://mijngemeentewebsite.nl/atlas/hondenbeleid

<img src="/uploads/822f1c6ac667ca0182b37874c68b322b/hondenbeleid.png" alt="hondenbeleid" width="500"/>



De volgende velden moeten worden ingevuld bij het toevoegen van een Thema:
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


#### AUTHENTICATIE EN AUTORISATIE

##### Groepen
##### Versie 2.2.4: Deze functie is voor toekomstig gebruik!
Binnen authenticatie en autorisatie kunnen gebruikersgroepen aangemaakt en bewerkt worden. Per groep kunnen rechten worden toegekend voor bewerkingen binnen Atlas en de toegang tot data. 
Versie 2.2.4: Deze functie is voor toekomstig gebruik, er is nog geen koppeling met Atlas gebruikersgroepen

<img src="/uploads/993faa161f2e10a09bc77a72533c1536/auth-en-autorisatie.png" alt="Authenticatie en autorisatie" width="700"/>

Per groep kunnen rechten worden toegekend. Klik in het "Authenticatie en autorisatie" scherm naast het groene plus teken op Toevoegen om een groep toe te voegen. In het "groep toevoegen" scherm kan nu een naam voor de nieuwe groep worden opgegeven en kunnen rechten voor deze nieuwe groep vanuit de linker kolom naar de rechter kolom worden verplaatst.

<img src="/uploads/abeaa04c8cd16b8477b2b775a15ec91b/groep-toevoegen.png" alt="Authenticatie en autorisatie: groep toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***












