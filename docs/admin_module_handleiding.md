# Handleiding Admin Module Atlas versie 2.2.4

## Deze handleiding beschrijft de werking van de Admin Module. In de Admin Module wordt de configuratie van atlas gedaan.

### Inhoud

* [INTRODUCTIE EN HOOFDSCHERM](#introductie-en-hoofdscherm)
* [AUTHENTICATIE EN AUTORISATIE](#authenticatie-en-autorisatie)
* [HOMEPAGE](#homepage)
* [USER_MANAGEMENT](#user_management)
* [WEBSERVICE](#webservice)

##### INTRODUCTIE EN HOOFDSCHERM

In de README.MD file wordt in de laatste stap een superuser aangemaakt. Met deze gebruiker kan in de adminmodule worden ingelogt zoals in de README.MD beschreven.
Let op dat de url eindigt met een /.

Het hoofdscherm **Websitebeheer** laat een aantal onderdelen zien die ingesteld kunnen worden.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/hoofdscherm.png" alt="Hoofdscherm Admin module" width="1000"/>


***
* [Naar boven](#inhoud)
***

##### AUTHENTICATIE EN AUTORISATIE
Binnen authenticatie en autorisatie kunnen gebruikersgroepen aangemaakt en bewerkt worden. Per groep kunnen rechten worden toegekend voor bewerkingen binnen Atlas en de toegang tot data. 
Versie 2.2.4: Deze functie is voor toekomstig gebruik, er is nog geen koppeling met Atlas gebruikersgroepen

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/auth-en-autorisatie.png" alt="Authenticatie en autorisatie" width="700"/>

Per groep kunnen rechten worden toegekend. Klik in het "Authenticatie en autorisatie" scherm naast het groene plus teken op Toevoegen om een groep toe te voegen. In het "groep toevoegen" scherm kan nu een naam voor de nieuwe groep worden opgegeven en kunnen rechten voor deze nieuwe groep vanuit de linker kolom naar de rechter kolom worden verplaatst.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/groep-toevoegen.png" alt="Authenticatie en autorisatie: groep toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***

##### HOMEPAGE
Binnen atlas bestaat de mogelijkheid om adressen binnen een kaart te selecteren. Dit kan door middel van de CTRL toets ingedrukt te houden en tegelijkertijd met de muis een gebied met adressen te selecteren. Ook kunnen adressen geselecteerd worden met behulp van de selectietool rechtsboven in het Atlas scherm. Deze adres-selecties worden op het scherm getoond maar kunnen ook gedownload worden. Binnen Atlas zelf worden deze selecties in de database opgeslagen. Via de "Saved Datasets" optie, kunnen deze selecties beheerd worden.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/saved-datasets.png" alt="Saved datasets" width="600"/>

Wanneer een "saved dataset" wordt geselecteerd, dan zal de inhoud in het JSON scherm getoond worden.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/saved-dataset-wijzigen.png" alt="Saved dataset wijzigen" width="600"/>

Ook is het mogelijk om via cut & paste zelf datasets toe te voegen voor eventueel toekomstig gebruik.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/dataset-toevoegen.png" alt="Dataset toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***

##### USER_MANAGEMENT
In user management bevindt zich het aanmaken en bewerken van Atlas gebruikers. Atlas gebruikers kunnen op hun beurt weer toegevoegd worden
aan een Atlas group. Het gebruikersbeheer heeft geen relatie met groepen in authenticatie en autorisatie.
Klik in het user management beheer scherm bij gebruikers op Toevoegen om een gebruiker toe te voegen.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/user-magement-beheer.png" alt="Gebruikersbeheer" width="600"/>

In het volgende scherm kan een gebruikersnaam en wachtwoord worden ingegeven. De gebruikersnaam moet 150 tekens of minder lang zijn. Alleen letters, cijfers en @/,/+/-/_ tekens zijn toegestaan. Aan het wachtwoord zijn de volgende beperkingen gebonden: 
* Uw wachtwoord mag niet te veel lijken op uw overige persoonlijke informatie. 
* Uw wachtwoord moet minstens 8 tekens lang zijn. 
* Uw wachtwoord mag geen veelgebruikt wachtwoord zijn. 
* Uw wachtwoord mag niet volledig uit cijfers bestaan.

Klik op Opslaan om deze gegevens naar de database te schrijven. Nu verschijnt een uitgebreid scherm waarin extra gebruikergegevens kunnen worden ingegeven of gewijzigd. Wanneer er ook groepen zijn aangemaakt, kan hier de gebruiker aan een of meerdere groepen worden toegevoegd. Houd 'Control', of 'Command' op een Mac, ingedrukt om meerdere items te selecteren.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/gebruiker-toevoegen.png" alt="gebruiker toevoegen" width="1400"/>

In het Gebruiker Wijzigen scherm kan uitgebreide gebruikersinformatie worden toegevoegd of gegevens gewijzigd.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/_gebruikerswijzigen2.png" alt="gebruiker wijzigen 2" width="1400"/>

In het Atlas Groep Toevoegen scherm kunnen groepen worden aangemaakt. Wanneer er ook gebruikers zijn aangemaakt kunnen deze hier aan de groep worden toegvoegd.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/atlas-groep-toevoegen.png" alt="atlas groep toevoegen" width="1400"/>

***
* [Naar boven](#inhoud)
***

##### WEBSERVICE

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/webservice-beheer.png" alt="Webservice beheer" width="600"/>

Binnen webservice kunnen Categorieën, kaartlagen en thema's worden toegevoegd.
Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond. Het klikken op een van de hoofdonderwerpen/categorieën
zorgt ervoor dat eronder de verschillende kaartlagen van die categorie worden getoond.
Bij het toevoegen van een kaartlaag wordt onder andere aangegeven onder welke categorie deze valt.
Categorieën worden getoond op alfabetische volgorde, onder Achtergrondkaarten en Luchtfoto's. Hou hier rekening mee bij het aanmaken van een categorie.

Categorieën \
<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/categorieenkopie.png" alt="categorieën" width="500"/>

Kaartlagen \
<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/kaartlagenkopie.png" alt="kaartlagen" width="500"/>


Thema's zijn verzamelde kaartlagen die samen over een bepaald onderwerp gaan. Bij het aanmaken van een thema worden de kaartlagen geselecteerd die bij dat thema horen. Een thema verschijnt niet in het Atlas scherm als aanklikbare menu-optie maar moet in de url balk worden meegegeven. Wanneer bijvoorbeeld een thema 'hondenbeleid' is aangemaakt waarin de kaartlagen 'hondenuitlaatplekken' en  'hondenbakken' zitten, dan kan de url om dit thema op te vragen er bijvoorbeeld zo uitzien: https://mijngemeentewebsite.nl/atlas/hondenbeleid

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/hondenbeleid.png" alt="hondenbeleid" width="500"/>


De volgende velden moeten worden ingevuld bij het toevoegen van een categorie:
* **Title:** (De naam zoals die in het viewer scherm van Atlas komt te staan, denk hierbij om de alfabetische volgorde)
* **Javascript type:** (default waarde: themelayer:true)
* **Gesloten thema** (Is deze categorie in alle omgevingen zichtbaar of alleen intern?)

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/categorie-toevoegen.png" alt="categorie toevoegen" width="500"/>


De volgende velden moeten worden ingevuld bij het toevoegen van een kaartlaag:
* **Layer_id:** (Een uniek ID dat de layer onderscheid van andere)
* **Title:** (De naam zoals die verschijnt in het viewer scherm van Atlas)
* **Layer_name:** (De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bv: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver)
* **Meta_naam:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Adressen(BAG))
* **Meta_soort:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Basisregistratie)
* **Meta_org:** ([Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Geoinformatie
* **Meta_bijgewerkt:** (De waarde wordt door Javascript geëvalueerd (Bijv:"01-01-2018",getDate("year"). Default: getDate("full"))
* **Opacity:** (default 0,9)
* **Visible:** (is deze layer zichtbaar in de viewer?)
* **Categorie:** (selecteer onder welke categorie deze layer komt)
* **ISqueryable:** (maak de layer zichtbaar in het zoekscherm binnen de viewer)
* **Popup attributes:** ([Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in dit pop-up venster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd)
* **Search fields:** (Selecteer de velden waar bij Zoeken op Data op gezocht kan worden)
* **Projection:** (standaard: EPSG:28992)
* **Url:** De URL van de layer (http://GEOSERVER_URL/wms?...) Het gebruikte endpoint (zie ook de<a href="https://docs.geoserver.org/stable/en/user/geowebcache/webadmin/defaults.html#gwc-webadmin-defaults">geoserver handleidng</a>)
* **Server type:** (standaard: geoserver)
* **Gesloten data:** (is de layer ook buiten het interne netwerk zichtbaar)
* **Gepubliceerd:** (Default: aan)
* **Alleen in een thema, niet in Atlas:** (Kaartlaag wordt niet in Atlas getoond, alleen als kaartlaag in een thema)
* **Owner:** (Wie is eigenaar van deze layer) 
* **Users:** (Welke gebruikers hebben toegang tot deze kaartlaag? (Deze functie is nog niet in gebruik))
* **Atlas groups:** ([Welke Atlas gebruikersgroepen hebben toegang tot deze kaartlaag? (Deze functie is nog niet in gebruik))
* **Ordening:** (uniek nummer dat de rangschikking binnen het viewer scherm bepaalt)

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/kaartlaag-toevoegen.png" alt="kaartlaag toevoegen" width="700"/>


De volgende velden moeten worden ingevuld bij het toevoegen van een Thema:
* **Title:** ([De naam zoals die ook bij de url ingegeven moet worden)
* **Layers:** (De layers die binnen het Thema vallen)
Houd 'Control', of 'Command' op een Mac, ingedrukt om meerdere kaartlagen te selecteren.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/thema-toevoegen.png" alt="Thema Toevoegen" width="700"/>

***
* [Naar boven](#inhoud)
***












