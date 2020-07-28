# Handleiding Admin Module Atlas versie 2.2.4

## Deze handleiding beschrijft de werking van de Admin Module. In de Admin Module wordt de configuratie van atlas gedaan.


In de README.MD file wordt in de laatste stap een superuser aangemaakt. Met deze gebruiker kan in de adminmodule worden ingelogt zoals in de README.MD beschreven.
Let op dat de url eindigt met een /.

Het hoofdscherm **Websitebeheer** laat een aantal onderdelen zien die ingesteld kunnen worden.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/hoofdscherm.png" alt="Hoofdscherm Admin module" width="1000"/>

##### AUTHENTICATIE EN AUTORISATIE
Binnen authenticatie en autorisatie kunnen gebruikersgroepen aangemaakt en bewerkt worden.

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/auth-en-autorisatie.png" alt="Authenticatie en autorisatie" width="700"/>

Per groep kunnen rechten worden toegekend. 

<img src="https://gitlab.com/purmerend/atlas/-/raw/admin-module-manual/docs/images/groep-toevoegen.png" alt="Authenticatie en autorisatie: groep toevoegen" width="700"/>


##### HOMEPAGE
Binnen homepage kunnen datasets toegevoegd en gewijzigd worden. Datasets moeten worden toegevoegd in JSON formaat

##### USER_MANAGEMENT
In user management bevindt zich het aanmaken en bewerken van Atlas gebruikers. Atlas gebruikers kunnen op hun beurt weer toegevoegd worden
aan een Atlas group.

##### WEBSERVICE
Binnen webservice kunnen Categorieën, kaartlagen en thema's worden toegevoegd.
Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond. Het klikken op een van de hoofdonderwerpen/categorieën
zorgt ervoor dat eronder de verschillende kaartlagen van die categorie worden getoond.
Bij het toevoegen van een kaartlaag wordt onder andere aangegeven onder welke categorie deze valt.
[Thema ontbreekt nog in de handleiding

]

De volgende velden moeten worden ingevuld bij het toevoegen van een categorie:
**Title:** (De naam zoals die in het viewer scherm van Atlas komt te staan)
**Javascript type:** ([nog toevoegen])
**Gesloten thema** ([nog toevoegen])

De volgende velden moeten worden ingevuld bij het toevoegen van een kaartlaag:
**Layer_id:** (Een uniek ID dat de layer onderscheid van andere)
**Title:** (De naam zoals die verschijnt in het viewer scherm van Atlas)EPSG:28992
**Layer_name:** ([nog toevoegen])
**Meta_naam:** ([nog toevoegen])
**Meta_soort:** ([nog toevoegen])
**Meta_org:** ([nog toevoegen])
**Meta_bijgewerkt:** ([nog toevoegen])
**Opacity:** (waarbij 0 doorzichtig is [klopt dit?])
**Visible:** (is deze layer zichtbaar in de viewer?)
**Categorie:** (selecteer onder welke categorie deze layer komt)
**ISqueryable:** (maak de layer zichtbaar in het zoekscherm binnen de viewer)
**Popup attributes:** ([nog toevoegen])
**Search fields:** ([nog toevoegen])
**Projection:** (standaard: EPSG:28992)
**Url:** (url van layer)
**Server type:** (standaard: geoserver)
**Gesloten data:** (is de layer ook buiten het interne netwerk zichtbaar)
**Gepubliceerd:** ([nog toevoegen])
**Alleen in een thema, niet in Atlas:** (Kaartlaag wordt niet in Atlas getoond, alleen als kaartlaag in een thema)
**Owner:** (Wie eigenaar van deze layer)
**Users:** ([nog toevoegen])
**Atlas groups:** ([nog toevoegen])
**Ordening:** (uniek nummer dat de rangschikking binnen het viewer scherm bepaalt)


De volgende velden moeten worden ingevuld bij het toevoegen van een Thema:
**Title:** ([nog toevoegen])
**Layers:** (De layers die binnen het Thema vallen)

![thema-toevoegen](https://gitlab.com/purmerend/atlas/uploads/83378d840b94f66f299bfe3cf19b7575/thema-toevoegen.png)

![wijzig-atlas-groep](https://gitlab.com/purmerend/atlas/uploads/c7edbce90fd4526f35a82d6b7a285de1/wijzig-atlas-groep.png)

![user-magement-beheer](https://gitlab.com/purmerend/atlas/uploads/53a263e3428df613fc08d3faa05d7ba8/user-magement-beheer.png)

![wijzigen-dataset1](https://gitlab.com/purmerend/atlas/uploads/c40b279b26a3117febfb18102b64b069/wijzigen-dataset1.png)



![wijzig-groep](https://gitlab.com/purmerend/atlas/uploads/b1f275d96e5bab81070237ff8c32c1ac/wijzig-groep.png)



![webservice-beheer](https://gitlab.com/purmerend/atlas/uploads/cfcd96dc0a3fc25b256d78b8731dc806/webservice-beheer.png)

![_gebruikerswijzigen2](https://gitlab.com/purmerend/atlas/uploads/21fd98949d8a147ddd45e0a1a2aa6707/_gebruikerswijzigen2.png)

![gebruikerswijzigen](https://gitlab.com/purmerend/atlas/uploads/9c6525271d34d18e39df34675d68b1a3/gebruikerswijzigen.png)



