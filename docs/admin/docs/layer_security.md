<base target="_blank">
## Beveiliging / per layer security

De kracht van Atlas is dat het zowel binnen een organisatie (intern) als extern (internet) gebruikt kan worden. Het grote voordeel hiervan is dat zowel inwoners van een gemeente als de medewerkers van de gemeente naar dezelfde informatie kijken. Het zorgt voor openheid richting inwoners.
Wanneer het gaat om (privacy)gevoelige data, moet dat echter wel goed beveiligd kunnen worden. Dit is waar we per layer security voor gebruiken. Hieronder wordt besproken hoe dat binnen Atlas kan.

Atlas maakt als databron gebruik van [Geoserver](https://geoserver.org). Zowel Atlas als Geoserver zijn goed te beveiligen tegen ongeoorloofde toegang tot data. De beveiligingsopties van Atlas en Geoserver zijn ook te combineren om zo specifieke toegangsregels te kunnen toepassen. Met behulp van [Filter-Proxy](https://github.com/delta10/filter-proxy) kunnen de beveiligingsopties van Atlas en Geoserver gecombineerd worden

Toegang tot Atlas is op meerdere niveaus te beveiligen. Kaartlagen kunnen zo ingesteld worden dat ze door iedereen bekeken kunnen worden of alleen binnen het lokale netwerk. Binnen het lokale netwerk kan worden aangegeven dat een kaartlaag door alle of alleen door een specifieke groep medewerkers bekeken mag worden. Daarnaast is het mogelijk om voor kaartlagen te bepalen of ze ook bewerkt mogen worden; dit houdt in dat objecten op kaartlaag niveau toegevoegd, bewerkt en/of verwijderd kunnen worden. Dit recht kan je per kaartlaag of autorisatie toekennen aan een losse groep met gebruikers of voor iedereen die ingelogd is.

Atlas kan zowel met een externe Geoserver als met een interne Geoserver werken. Met extern wordt bedoelt ‘in de cloud’, met intern wordt bedoelt ‘binnen het lokale netwerk’.

Om data binnen Geoserver af te schermen kan gebruikt gemaakt worden van de verschillende opties die Geoserver hiervoor biedt. Staat Geoserver ook nog achter een firewall (intern) dan is dit nog een extra beveiligingslaag voor (privacygevoelige)data.

De gebruikersinterface van Atlas is altijd toegankelijk. Toegang tot data is te beperken via:

- De gebruikte bron (Geoserver)
- Gebruikersrechten-instellingen binnen Atlas (na inloggen)
- Rechten per gebruikersgroep en/of kaartlaag instellen via Filter-Proxy
- De fysieke locatie van de brondata

Geoserver heeft een goede [handleiding](https://docs.geoserver.org/latest/en/user/security/index.html) waarin de beveiliging besproken wordt. Hieronder wordt besproken hoe Geoserver ingericht kan worden om via Filter-proxy binnen Atlas gebruik te maken van per-layer-security.

<img src="../images/filter-proxy.png" alt="rechtsboven" title="config.yaml" width="500" />

##Configuratie Filter-proxy

Installeer Filter-Proxy op de server waar Geoserver draait (Windows of Linux). Pas [config.yaml](https://github.com/delta10/filter-proxy/blob/main/config.yaml) aan voor de eigen omgeving. Laat de toegang tot Geoserver lopen via Filter proxy

- Maak een account aan binnen Geoserver dat gelijk is aan ‘username’ binnen Filter-proxy config.yaml. In dit voorbeeld is de username: filter-proxy.
  <img src="../images/config-yaml.png" alt="rechtsboven" title="config.yaml" width="350" />
- Zet het poortnummer bij ListenAddress in config.yaml op 443.
  <img src="../images/config-yaml2.png" alt="rechtsboven" title="config.yaml" width="350" />

##Configuratie Geoserver

- Maak een Role aan binnen Geoserver die gelinkt is aan de Filter-proxy user (Bijvoorbeeld user: filter-proxy en Role: FILTER_PROXY)  
  <img src="../images/roles.png" alt="rechtsboven" title="config.yaml" width="350" />  
  <img src="../images/users-geoserver.png" alt="rechtsboven" title="config.yaml" width="350" />  
  <img src="../images/user-properties.png" alt="rechtsboven" title="config.yaml" width="350" />  
  Maak eventueel een aparte workspace aan waar alleen de Filter-proxy user toegang toe heeft. In dit voorbeeld: protected  
  <img src="../images/workspaces.png" alt="rechtsboven" title="config.yaml" width="350" />

Stel bij het aanmaken van de kaartlaag in het tabblad beveiliging in welke groep welke rechten heeft op deze kaartlaag, wil je objecten op de kaartlaag kunnen bewerken, verwijderen en/of toevoegen dan moet de schrijf rechten voor betreffende gebruiker ook toegekend worden. Andersom is het ook mogelijk om via het menu Security / Data / Data Security de rechten in te stellen per groep of kaartlaag of de rechten voor meerdere kaartlagen via wildcards in te stellen.

<img src="../images/data_security.png" alt="rechtsboven" title="config.yaml" width="650" />

##Configuratie Atlas

Rechten per kaartlaag werkt als volgt:

Binnen Atlas moet een bron aangemaakt zijn die via Filter-proxy de data binnenhaalt. Deze bron heeft ‘Vereis inlog voor deze bron’ en ‘verstuur authenticatie naar bron’ aanstaan.
<img src="../images/bron-wijzigen.png" alt="rechtsboven" title="config.yaml" width="350" />  
De te beveiligen kaartlaag moet deze bron gebruiken.
Onder Toegang: ‘Alleen intern zichtbaar’ en ‘vereis inlog’ aanzetten.
Selecteer de gebruikersgroep die deze kaartlaag mag zien. De gebruikersgroep moet in Geoserver en Atlas bestaan. Geef in Atlas de gebruikers toegang tot de groep.
<img src="../images/toegang.png" alt="rechtsboven" title="config.yaml" width="850" />  
Wil je een bepaalde groep en/of alle ingelogde gebruikers toegang geven tot het bewerken, verwijderen en/of toevoegen van objecten op de kaartlaag dan kan dit via schrijf groepen bij kaartlagen en/of de optie "Ingelogde gebruikers kunnen kaartlaag bewerken".

Wanneer binnen de kaartlaaginstellingen filter-proxy als bron is geselecteerd dan kan de laag niet uit de lijst geselecteerd worden. De laagnaam moet dan handmatig bij Laagnaam worden ingevuld. Formaat: _Omgeving:laagnaam_. Dus bijvoorbeeld: _protected:mijnvertrouwelijkekaartlaag_.

<img src="../images/filter-proxy-kaartlaag.png" alt="rechtsboven" title="config.yaml" width="850" />
