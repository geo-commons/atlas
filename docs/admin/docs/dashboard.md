---
## DASHBOARD
---   

Via het dashboard kom je bij de verschillende onderdelen die ingesteld kunnen worden.


<img src="../images/dashboard.png" alt="Hoofdscherm Admin module" width="700"/>


---
## KAARTEN
---

Kaarten zijn verzamelingen kaartlagen die samen over een bepaald onderwerp gaan. Om een kaart samen te stellen worden kaartlagen geselecteerd die bij die kaart horen.
Een kaart verschijnt niet in het Atlas hoofdscherm scherm. Bij het aanmaken van een kaart wordt als het ware een aparte instantie van Atlas gecreëerd met een beperkter aantal kaartlagen en beperktere functionaliteit. Wanneer bijvoorbeeld een kaart 'hondenbeleid' is aangemaakt waarin de kaartlagen 'hondenuitlaatplekken' en 'hondenbakken' zitten, dan kan de url om de kaart op te vragen er bijvoorbeeld zo uitzien: https://mijngemeentewebsite.nl/atlas/maps/hondenbeleid

<img src="../images/hondenbeleid.png" alt="hondenbeleid" width="500"/>

Om een kaart aan te maken klik je in het Kaarten menu op de knop Nieuwe kaart.
Vul de twee velden in. De titel mag uit meerdere woorden bestaan. Het veld Kort kenmerk mag geen spaties bevatten, wel (liggende)streepjes. Dit veld moet ook een unieke waarde hebben.
Klik op Opslaan en openen wanneer beide velden zijn ingevuld.



<img src="../images/nieuwe_kaart.png" alt="Kaart Toevoegen" width="800"/>  

In het kaartmenu kunnen de verschillende opties voor een kaart geconfigureerd worden.  
Een optie die aangeklikt wordt, is direct in het voorbeeldscherm te zien.
Sommige opties hebben een submenu met keuzes, dit wordt zichtbaar nadat de optie is aangevinkt.

---
## Kaart lagen
---  

<img src="../images/kaartmenu.png" alt="Kaart Toevoegen" width="500"/>

 
- **Titel**. Deze kan eventueel nog worden aangepast. Let hierbij op dat de URL wel de originele naam zal bevatten.  
- [**Lagen**](#kaart-lagen). Hier kunnen de beschikbare kaartlagen worden gekozen en geconfigureerd.  
- **Toon** zoekbalk  
De zoekbalk zoals die linksboven in het Atlas scherm getoond wordt.  
<img src="../images/zoekbalk.png" alt="zoekbalk" width="400"/>
- **Toon** dataweergave  
<img src="../images/dataweergave.png" alt="zoekbalk" width="50"/>
- **Selecteer** gebied  
<img src="../images/selecteer_gebied.png" alt="zoekbalk" width="50"/>
- **Opmeten**  
<img src="../images/opmeten.png" alt="zoekbalk" width="50"/>
- **Meer opties**  
<img src="../images/meer_opties.png" alt="zoekbalk" width="50"/>
- **GPS knop**  
<img src="../images/gps_knop.png" alt="zoekbalk" width="50"/>
- **Zoomfunctie**  
<img src="../images/zoomfunctie.png" alt="zoekbalk" width="50"/>
- **Toon schaal**  
<img src="../images/toon_schaal.png" alt="zoekbalk" width="100"/>
- **Prikker bij klik**  
Toont het 'prikker' symbool wanneer ergens op de kaart geklikt wordt.  
<img src="../images/prikker_bij_klik.png" alt="zoekbalk" width="50"/>
- **Basislagen**  
<img src="../images/basislagen.png" alt="zoekbalk" width="50"/>
- **Lagenlijst**  
Bij lagenlijst kan na aanvinken gekozen worden om de zoekbalk lagenlijst te verbergen en om een versimpelde weergave van de lagenlijst te laten zien.  
<img src="../images/lagenlijst.png" alt="zoekbalk" width="50"/>
- **Legenda**  
<img src="../images/legenda.png" alt="zoekbalk" width="50"/>
- **Lijstweergave**  
De lijstweergave kan na aanvinken in het submenu verder geconfigureerd worden.  
<img src="../images/lijstweergave.png" alt="zoekbalk" width="100"/>
- **Detailweergave**  
<img src="../images/detailweergave.png" alt="zoekbalk" width="100"/>
- **Filters**  
De filterfunctie kan na aanvinken in het submenu verder geconfigureerd worden.  
<img src="../images/filters.png" alt="zoekbalk" width="100"/>

Klik op opslaan om de gemaakte keuzes te bewaren.



---
## CONFIGURATIE
---

Hier kunnen de globale instellingen gedaan worden die in Atlas getoond worden.  

### Organisatie  

- **Naam Organisatie**  
De naam van de organisatie die getoond moet worden.

- **Huidige logo**  
Deze afbeelding komt linksboven in Atlasscherm te staan.  

- **Favicon URL**  
Verwijzing naar een icon. Dit wordt getoond in de tabbladen van de browser.  
Favicons kunnen zijn PNG, SVG, JPG of ICO, waarbij SVG formaat vector georiënteerd is.  
Groote kan varieren van 16x16, 32x32, 48x48, 96x96 tot 144x144  

### Kaartconfiguratie  

- **Centrum X-coördinaat**  
Het centrum X-coördinaat van de opstartpositie.  

- **Centrum Y-coördinaat**  
Het centrum Y-coördinaat van de opstartpositie. 

- **Zoomniveau**  
Het zoomniveau van de opstartpositie.

- **Doorzoek deze gemeentes**  
Een komma-gescheiden lijst van gemeenten om adressen in te zoeken (voor auto-aanvulfunctionaliteit).  

- **Standaard kaartgebied**  
Configureer een gebied dat standaard uitgelicht wordt op de kaart.  

### Matomo  

- **Matomo Site Url**  
- **Matomo Site Id**  
[Matomo](https://github.com/matomo-org/matomo) kan gebruikt wordenom statistieken bij te houden. Vul in deze velden de benodigde informatie in.  

### Features  

- **Portaal functionaliteit**  
Zet de portaalfunctionaliteit aan of uit als startscherm. In het portaal kunnen bijvoorbeeld kaarten worden aangeboden.  
- **Print functionaliteit** 
Geef de mogelijkheid om een PDF bestand van het zichtbare scherm te maken in verschillende resoluties.  
- **Tekenfunctionaliteit**  
Geef de mogelijkheid om in de zichtbare kaart te tekenen en dit op te slaan als URL.    
- **Zet oude beheerpnaeel uit**  
Tijdelijke feature in de overgangsperiode van de oude naar de nieuwe admin module.  





---
## GEBRUIKERSBEHEER
---

In het gebruikersbeheerscherm bevindt zich het aanmaken en bewerken van Atlas gebruikers. Atlas gebruikers kunnen op hun beurt weer toegevoegd worden aan een Atlas groep.  
Groepen kunnen aangemaakt worden om toegang tot lagen te configureren.

In het gebruikersscherm kan een gebruiker worden toegevoegd of bewerkt. Voor een nieuwe gebruiker moet een gebruikersnaam en wachtwoord worden ingegeven. De gebruikersnaam kan 150 tekens lang of minder zijn. Alleen letters, cijfers en @/,/+/-/\_ tekens zijn toegestaan. Aan het wachtwoord zijn de volgende beperkingen gebonden:

- Uw wachtwoord mag niet te veel lijken op uw overige persoonlijke informatie.
- Uw wachtwoord moet minstens 8 tekens lang zijn.
- Uw wachtwoord mag geen veelgebruikt wachtwoord zijn.
- Uw wachtwoord mag niet volledig uit cijfers bestaan.

Klik op Opslaan om deze gegevens naar de database te schrijven. Nu verschijnt een uitgebreid scherm waarin extra gebruikergegevens kunnen worden ingegeven of gewijzigd. Wanneer er ook groepen zijn aangemaakt, kan hier de gebruiker aan een of meerdere groepen worden toegevoegd. Houd 'Control', of 'Command' op een Mac, ingedrukt om meerdere items te selecteren.

<img src="../images/gebruiker-toevoegen.png" alt="gebruiker toevoegen" width="1400"/>

In het Gebruiker Wijzigen scherm kan uitgebreide gebruikersinformatie worden toegevoegd of gegevens gewijzigd.

<img src="../images/_gebruikerswijzigen2.png" alt="gebruiker wijzigen 2" width="1400"/>

---
### GROEPEN
---

In het Atlas Groep Toevoegen scherm kunnen groepen worden aangemaakt. Wanneer er ook gebruikers zijn aangemaakt kunnen deze hier aan de groep worden toegvoegd.

<img src="../images/atlas-groep-toevoegen.png" alt="atlas groep toevoegen" width="1400"/>

---
## BRONNEN
---

Binnen Bronnen kunnen meerdere endpoints geconfigureerd worden. Wanneer bijvoorbeeld een Geoserver met meerdere omgevingen gebruikt wordt of als ook externe kaartlagen gebruikt worden,
kan dit handig zijn. Bronnen kunnen toegevoegd, bewerkt of verwijderd worden.

<img src="../images/bronnen1.png" alt="bronnen" width="400"/>

Klik op een bron om deze te bewerken of te verwijderen. Om meerdere bronnen te verwijderen kunnen deze geselecteerd worden, kies bij Actie "Geselecteerde Bronnen verwijderen".
Klik links bovenin op "BRON TOEVOEGEN" om een nieuwe bron toe te voegen.

<img src="../images/bronnen2.png" alt="bronnen" width="400"/>

Vul bij een nieuwe bron een titel in voor deze bron en het endpoint als Url. Voor de achtergrondkaarten van PDOK is dit bijvoorbeeld: https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0.

<img src="../images/bronnen3.png" alt="bronnen" width="400"/>

De bewerkingsgeschiedenis kan bekeken worden door op de knop "Geschiedenis" te klikken.

---
<div id="categorieen">
<h2>CATEGORIEËN</h2> 
</div>
---

Categorieën zijn de hoofdonderwerpen zoals die links in het scherm van Atlas worden getoond. Het openklikken van een hoofdonderwerp/categorie
zorgt ervoor dat eronder de verschillende kaartlagen van die categorie in de legenda worden getoond.
Bij het toevoegen van een kaartlaag wordt aangegeven onder welke categorie deze valt.

<img src="../images/categorieen.png" alt="categorieën" width="400"/>

De volgende velden moeten worden ingevuld bij het toevoegen van een categorie:

- **Titel:** (De naam zoals die in het viewer scherm van Atlas komt te staan)
- **Sortering:** (default waarde: 0)

<img src="../images/categorie-toevoegen.png" alt="categorie toevoegen" width="500"/>

---
## KAARTLAGEN
---

Kaartlagen zijn de datasets die binnen Atlas ontsloten worden.
Kaartlagen kunnen worden toegevoegd aan Atlas en/of aan één of meerdere kaarten.

Klik op Nieuwe laag in het kaartlagen scherm om een nieuwe kaartlaag aan te maken.  
Vul de drie velden in en klik daarna op Opslaan en openen om de nieuwe kaartlaag te configureren.  

- **Titel** is het veld dat getoond gaat worden in het kaartlagenmenu van Atlas.  
- [**Categorie**](#categorieen) is de groep waaronder de kaartlaag zichtbaar zal zijn in het kaartlagenmenu van Atlas. Kies hier vanuit het pull-down menu een categorie.  
- [**Bron**](#bronnen) is een eerder aangemaakt endpoint waarvanuit de laag geserveerd wordt. Dit kan vanuit een eigen Geoserver zijn maar ook een externe bron. 

<img src="../images/configureer_nieuwe_kaartlaag.png" alt="Kaart Tagoevoegen" width="700"/>



- **Titel:** (De naam zoals die verschijnt in de legenda van Atlas. De invoer mag geen 'speciale' tekens bevatten)
- **Kort kenmerk:** (Een uniek ID dat de layer onderscheid van andere.
- **Categorie:** (selecteer onder welke categorie deze layer komt)
- **Gepubliceerd:** (wordt de laag gepubliceerd of niet. deze optie kan gebruikt worden om de laag tijdens het configureren nog niet aan Atlas aan te bieden, of om deze snel (tijdelijk) uit Atlas te verwijderen zonder dat de volledige kaartlaagconfiguratie verwijderd hoeft te worden.)(Default: uit)

- **Bron:** (Selecteer er één zoals die bij 'Bronnen' zijn geconfigureerd).
- **Laagnaam:** (De naam van de kaartlaag zoals die in Geoserver geconfigureerd is, bv: topp:BAG_Verblijfseenheid. Topp is hier de naam van de omgeving binnen Geoserver.)
- **Brontype:** (Selecteer het type voor deze laag)
- **Projectie:** (De projectie waarin de kaartlaag bevraagd wordt. Default: EPSG:28992)
- **Server type:** (standaard: geoserver)

- **Transparantie:** (default 0,9)

- **Meta_naam:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Adressen(BAG))
- **Meta_soort:** (Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Basisregistratie)
- **Meta_org:** ([Wanneer meta data wordt bijgehouden, kan hier een omschrijving worden ingevuld, bv: Geoinformatie
- **Meta_bijgewerkt:** (De waarde wordt door Javascript geëvalueerd (Bijv:"01-01-2018",getDate("year"). Default: getDate("full"))
- **Is basislaag:** (Aanzetten als de laag als achtergrondlaag moet dienen)
- **Is standaard zichtbaar:** (Eigenlijk zelfde als hierboven maar komt bovenop de basislaag)
- **Toon laag alleen in een themakaart:** (Kaartlaag wordt niet in Atlas getoond, alleen als kaartlaag in de kaarten waaraan deze is toegevoegd. Wanneer deze optie niet is aangevinkt is de laag zowel in een kaart als in het hoofdscherm zichtbaar)
- **Kan doorzocht worden:** (maak het mogelijk de laag te bevragen door in de kaart te klikken (popup attriutes) én maak de layer zichtbaar in de zoekfunctie )
- **Toon deze velden:** ([Bij klikken op een object in de kaart, verschijnt een pop-up venster met uitgebreide informatie. Geef in dit veld op welke velden in dit pop-up venster verschijnen. Dit zijn de veldnamen zoals in Geoserver gedefiniëerd. Als dit leeg wordt gelaten worden alle attributen getoond.)
- **Doorzoek deze velden:** (Selecteer de velden waar bij Zoeken op Data op gezocht kan worden. Als dit leeg gelaten wordt, worden alle attributen zoekvelden.) 

Bereik minimum en maximum kunnen ingevuld worden om een bounding-box te configureren. Dit kan handig zijn wanneer een kaartlaag maar één of een paar objecten toont die dicht bij elkaar liggen, er kan dan direct ingezoomd worden naar dit gebied.    

- **Bereik minimum x:** (Dit is de X waarde van het coördinaat linksonder. Vul een geldige RD waarde in)  
- **Bereik minimum y:** (Dit is de Y waarde van het coördinaat linksonder. Vul een geldige RD waarde in)  
- **Bereik maximum x:** (Dit is de X waarde van het coördinaat rechtsboven. Vul een geldige RD waarde in)  
- **Bereik maximum y:** (Dit is de Y waarde van het coördinaat rechtsboven. Vul een geldige RD waarde in) 

Wanneer het zoomniveau wordt ingevuld zal de kaartlaag greyed-out worden wanneer te ver uitgezoomd (minimum) of te ver inzoomd (maximum) is. Wanneer de kaartlaaggreyed-out is verschijnt een vergrootglas-icoon naast de kaartlaagnaam. Klikken hierop laat de kaartlaag in- of uitzoomen naar het niveau waar de objecten getoond worden.  
 
- **Zoomniveau minimum:** (Vul in om de laag inactief te maken wanneer de weergave buiten het zoomniveau ligt) 
- **Zoomniveau maximum:** (Vul in om de laag inactief te maken wanneer de weergave buiten het zoomniveau ligt) 

Om verschillende stijlen met één kaartlaag te kunnen gebruiken, kan hier een stijlbestand worden ingevuld. Het stijlbestand waarmee de kaartlaag in Geoserver is geconfigureerd wordt hiermee overruled. Het stijlbestand dat hier wordt ingevuld moet net als het originele stijlbestand op de Geoserver staan.  

  

- **Stijl:** (Voeg een stijlbestand in Geostyler of SLD formaat toe. Hiermee wordt de WFS stijl in Geoserver overruled) 
- **Vriendelijke veldnamen:** (In JSON formaat kunnen hier te tonen veldnamen aangepast worden. Bijvoorbeeld:   
{  
  "veldnm1": "Veldnaam 1",  
  "v2": "Veldnaam 2",  
  "v_3": "Veldnaam 3"  
}  

!!! warning "Waarschuwing"

    Wanneer JSON formaat gekopieerd wordt (bijvoorbeeld bovenstaande code naar Atlas), dan kan de characterset veranderen. Dit zorgt ervoor dat aanhalingstekens niet herkent worden en de code niet geaccepteerd wordt.  


Overigens krijgen lowercase veldnamen standaard een hoofdletter binnen Atlas. Een liggend streepje (underscore) wordt omgezet naar een spatie.    

- **Naam:** (Vul een naam in voor de laag als metadata. Deze informatie verschijnt wanneer op het ⓘ symbool wordt geklikt)  
- **Soort:** (Vul een categorie in voor de laag als metadata. Deze informatie verschijnt wanneer op het ⓘ symbool wordt geklikt)  
- **Organisatie:** (Vul de eigenaar van de betreffende data in. Deze informatie verschijnt wanneer op het ⓘ  symbool wordt geklikt)  
- **Laatst bijgewerkt:** (Datum laatst bijgewerkt. Deze informatie verschijnt wanneer op het ⓘ  symbool wordt geklikt)  
- **Alleen intern zichtbaar:** (is de kaartlaag ook buiten het interne netwerk zichtbaar)  
- **Vereis inlog voor deze dataset:** (Wanneer deze optie is aangevinkt, dan verschijnt de laag met een slotje ten teken dat men moet inloggen om de laag te zien)  
- **Eigenaar:** (Wie is eigenaar van deze layer)  
- **Gebruikers:** (Welke gebruikers hebben toegang tot deze kaartlaag?
- **Groepen:** (Welke Atlas gebruikersgroepen hebben toegang tot deze kaartlaag? )
- **Gekoppelde Data:** (Met deze optie kunnen overeenkomstige gegevens van andere kaartlagen gekoppeld worden en zichtbaar gemaakt.  
  
  -- Titel: Omschrijving van de gekoppelde laag  
  -- Laag naam: Omgeving:laagnaam  
  -- URL: Endpoint van de laag.  
  -- Bronsleutel: Overeenkomstige veldnaam van de bronlaag   
  -- Doelsleutel: Overeenkomstige veldnaam van de te koppelen laag  
  -- Toon deze velden: Wanneer dit veld leeg blijft, worden alle velden getoond.)  

Sla de gegevens op na het aanmaken van een gekoppelde laag.

---
## VIEWERS
---

Binnen Atlas kunnen verschillende viewers geconfigureerd worden voor zogenaamde rondkijk of 360 graden foto's. Op dit moment zijn dat Street Smart van Cyclomedia, Google StreetView en Obliquo.
Voor Google StreetView is alleen een API key nodig. Voor Street Smart is ook een gebruikersnaam en wachtwoord naast de API key nodig.
