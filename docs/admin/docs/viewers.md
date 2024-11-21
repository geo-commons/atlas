Binnen Atlas kunnen diverse externe viewers worden ingesteld. Externe viewers worden gebruikt om rondkijkfoto's weer te geven. Zo kan Google Maps als externe viewer worden gebruikt.
Een geconfigureerde externe viewer wordt geactiveerd op het moment dat op de Rondkijkfoto knop wordt geklikt.  
<img src="../images/rondkijkfoto.png" alt="Knop Rondkijkfoto" width="50"/>  
!!! info  

    De rondkijkfoto wordt pas getoond nadat op een locatie in de hoofdkaart is geklikt.  

Het Viewers scherm toont de verschillende geconfigureerde viewers.
<img src="../images/viewers.png" alt="Viewers configuratiescherm" width="900"/>   

Klik op 'Nieuwe viewer' om een externe viewer te configureren.  
<img src="../images/nieuwe_viewer.png" alt="Nieuwe viewer" width="900"/>  

Vul bij Label de titel van de viewer in die in het viewermenu getoond moet worden en klik daarna op 'Opslaan en openen'.
In het 'Viewer wijzigen' scherm kunnen de verdere benodigde instellingen gedaan worden.  

### Algemene gegevens  

- **Label**  
Het label zoals dat in het vorige menu is ingevuld.
- **Sortering**  
De volgorde van de viewers die getoond worden in het Viewers menu van het Atlas hoofdscherm. Hierbij is 0 het eerste item dat weergegeven zal worden.  
<img src="../images/volgorde_viewers.png" alt="Volgorde viewers" width="100"/>   

!!! Alert "Let op" 

    Wanneer bij één geconfigureerde viewer de volgorde is ingegeven, dan moet dit bij alle viewers gedaan worden.  


### Viewer instellingen  

- **Type**  
Selecteer hier het type viewer.
	- **Google Maps**  
		De viewer van Google  
	- **Street Smart**  
		De viewer van Cyclomedia  
	- **Obliquo**  
		De viewer van Obliquo Cloud  
	- **iFrame**  
		Met deze optie kan een viewer embedded worden die een URL met het formaat x={coördinaat}&y={coördinaat} accepteert.
	- **Knop naar een nieuw tabblad**  
		Kies deze optie wanneer een viewer in een nieuwe tabblad geopend moet worden. Standaard wordt het viewer scherm in de bovenste helft van het Atlas hoofdscherm getoond
- **Username**  
Vul hier de gebruikersnaam in voor toegang naar de viewer.
- **Password**  
Vul hier het wachtwoord in voor toegang naar de viewer.
- **Api Key**  
Vul hier de API key in voor toegang naar de viewer. 
- **URL**    
Vul hier de URL in die toegang geeft tot de viewer.
- **Is oblique** 
Wanneer deze optie is aangevink, wordt de viewer onder een apart knopje in het menu getoond. Standaard wordt nu een obliquebeeld getoond (state=oblique).  
<img src="../images/oblique_viewer.png" alt="Oblique viewer" width="70"/>   
De viewer verschijnt nu niet meer in het viewermenu van het Atlas hoofdscherm.   
<img src="../images/volgorde_viewers.png" alt="Volgorde viewers" width="100"/> 

### Toegang

- **Alleen zichtbaar voor ingelogde gebruikers en interne omgeving.**
Selecteer deze optie wanneer de viewer alleen aan de interne organisatie getoon mag worden. Standaard: _Aan_

!!! Alert "Let op" 

    Hou er rekening mee dat de gebruikersnaam, het wachtwoord of de API key gedeeld wordt met het publieke internet op het moment dat deze optie uit staat.  
