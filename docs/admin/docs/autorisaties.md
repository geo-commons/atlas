Binnen autorisaties kan geconfigureerd worden welke data van een API verbinding worden doorgegeven aan een groep.
Binnen het veld Resource kan gebruikt gemaakt worden van [regular expressions](https://en.wikipedia.org/wiki/Regular_expression).  
Een gebruikte bron binnen Autorisaties dient te verwijzen naar een API.

### Toegang

Via toegang valt te regelen wie wel en geen toegang hebben tot een bron of kaartlaag, ga hier zorgvuldig mee om.

- **Ingelogde gebruikers kunnen resource of laag bewerken:**
    Wanneer deze optie is ingeschakeld, houdt dit voor nu in dat alle ingelogde gebruikers binnen Atlas objecten op de kaartlaag kunnen muteren, dat wil zeggen: **toevoegen**, **bewerken** en/of **verwijderen**. Dit kan via zowel de kaartlaag module als de autorisatie module geregeld worden. Op bronnen heeft dit op dit moment nog geen betrekking, waar er nog geen mogelijkheden zijn in Atlas om data binnen bronnen te kunnen muteren.

    Wil je dat gebruikers deze acties kunnen uitvoeren, dan zijn er twee mogelijkheden:

    1. **Schakel deze optie in**  
    Hiermee krijgen alle ingelogde gebruikers bewerkingsrechten op de kaartlaag.

    2. **Gebruik schrijfgroepen**  
    In plaats van algemene toegang kun je specifieke gebruikers of groepen schrijfrechten geven via:
       - De instellingen van de **kaartlaag**
       - De instellingen binnen de **autorisatie**-module

    >   💡 Tip: Gebruik schrijfgroepen als je meer controle wilt over wie wijzigingen mag aanbrengen.

- **Lees groepen:** Onder "beschikbare groepen" staat een lijst met groepen die beschikbaar zijn binnen de Atlas omgeving, onder "geselecteerde groepen" staat een lijst met groepen die toegang hebben tot de kaartlaag.
- **Schrijf groepen:** Onder "schrijf groepen" staat een lijst met groepen die beschikbaar zijn binnen de Atlas omgeving, onder "geselecteerde groepen" staat een lijst met groepen die toegang hebben tot het muteren van objecten op de kaartlaag of bron (toevoegen, bewerken en/of verwijderen van objecten). 