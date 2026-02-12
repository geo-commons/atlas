Binnen Tabellen worden de API-bronweergaven geconfigureerd. Binnen Atlas kunnen meerdere tabellen geconfigureerd worden voor verschillende bronnen. Tabellen kunnen worden toegevoegd, bewerkt en verwijderd.

Klik op "Nieuwe tabel" om een tabel toe te voegen. Vul de titel in, deze verschijnt in het hoofdmenu onder tabellen. Het veld "Kort kenmerk" moet een unieke waarde hebben en mag geen spaties bevatten. Vul bij de BRON de bron in waaruit de tabeldata moet komen.

### Algemene gegevens
- **Titel**  
  Dit is de titel zoals ingegeven bij het aanmaken van de tabel.

- **Kort kenmerk**  
  Dit is het korte kenmerk zoals ingegeven bij het aanmaken van de tabel.

### Bron
- **Bron**  
  In dit selectieveld kun je een tabelbron kiezen uit de bronnen die binnen Atlas geconfigureerd zijn. Deze bron wordt gebruikt om de tabeldata op te halen in de tabelweergave.

- **Endpoint**  
  Dit is het endpoint dat gebruikt wordt om de data van de bron op te halen. Voorbeeld voor de bron "KVK" waarbij als bron de URL "https://api.kvk.nl" is ingesteld: "/api/v2/zoeken"

- **Bron methode**  
  Kies hier uit "GET" of "POST". Wanneer je data wilt ophalen vanuit een bron in je tabel, wordt over het algemeen de "GET" methode gebruikt.

### Tabel Instellingen
Onder tabelinstellingen stel je in hoe je tabel weergegeven moet worden in de tabelweergave. Dit kun je configureren op basis van hoe een response vanuit je gewenste bron eruitziet. Als voorbeeld nemen we een response van de KVK test API:

```json
{
  "pagina": 1,
  "resultatenPerPagina": 1,
  "totaal": 992,
  "volgende": "https://api.kvk.nl/test/api/v2/zoeken?pagina=2&resultatenperpagina=1",
  "resultaten": [
    {
      "kvkNummer": "90002148",
      "naam": "Free Stathex",
      "type": "rechtspersoon",
      "links": [
        {
          "rel": "basisprofiel",
          "href": "https://api.kvk.nl/test/api/v1/basisprofielen/90002148"
        }
      ]
    }
  ],
  "links": [
    {
      "rel": "self",
      "href": "https://api.kvk.nl/test/api/v2/zoeken?pagina=1&resultatenperpagina=1"
    }
  ]
}
```

- **Veldnaam van lijst**  
  Met dit veld configureer je uit welk response-attribuut de data uit je bron komt. In het KVK-voorbeeld is dit het attribuut "resultaten". Het is mogelijk om in dit veld ook de verwijzing te leggen naar geneste velden, zoals "resultaten[0].links". Hiermee zou de getoonde lijst opgebouwd worden uit de objecten die in de eerste lijst met attribuutnaam "links" in het "resultaten" object staan in het KVK-voorbeeld.

- **Veldnaam van pagina**  
  Met dit veld configureer je met welk response-attribuut de huidige pagina uit je bron komt. In het KVK-voorbeeld is dit het attribuut "pagina".

- **Veldnaam van items per pagina**  
  Met dit veld configureer je met welk response-attribuut het aantal items per pagina uit je bron komt. In het KVK-voorbeeld is dit het attribuut "resultatenPerPagina".

- **Veldnaam van totaal aantal items**  
  Met dit veld configureer je met welk response-attribuut het totaal aantal items vanuit je bron komt. In het KVK-voorbeeld is dit het attribuut "totaal".

- **Template van foutmelding**  
  Met dit veld configureer je met welk response-attribuut een foutmelding wordt teruggegeven, indien deze beschikbaar is. In een error response vanuit de KVK-bron is dit het attribuut "fout[0].omschrijving".

  - **Kopjes in lijstweergave**  
    Met dit veld configureer je welke kopjes in de tabelweergave staan. Voor het KVK-voorbeeld zouden dit bijvoorbeeld kunnen zijn:

    ```
    naam
    kvkNummer
    ```
  
    Let op: Voer hier enkel één veld per regel in.

  - **Velden in lijstweergave**  
    Met dit veld configureer je met welke velden de tabelrijen worden ingevuld. Het eerste attribuut komt onder het eerste kopje, het tweede attribuut onder het tweede kopje en de rest volgt op dezelfde manier. Voor het KVK-voorbeeld:

    ```
    {{ naam }}
    {{ kvkNummer }}
    ```

  - **Velden waarop gezocht kan worden**  
    Met dit veld configureer je op welke velden de tabel kan worden doorzocht. Met "name" als attribuut dat wordt gebruikt in de zoekopdracht naar de bron en "label" als attribuut dat wordt gebruikt voor op de tabelweergave pagina. Een voorbeeld voor de KVK-api:
  
    ```json
    [
      {"name": "naam", "label": "naam"},  
      {"name": "kvkNummer", "label": "kvkNummer"}
    ]
    ```

  - **Sortering**  
    De volgorde van de tabellen die getoond worden in het Tabellen-menu van het Atlas-portaalscherm. Hierbij is 0 het eerste item dat weergegeven zal worden.  

    !!! Alert "Let op"

        Wanneer bij één geconfigureerde tabel de volgorde is ingegeven, dan moet dit bij alle tabellen gedaan worden.  

### Toegang

Via toegang valt te regelen wie wel en geen toegang heeft tot het zien van een tabel. Ga hier zorgvuldig mee om.

- **Alleen intern zichtbaar:** Wanneer "alleen intern zichtbaar" aan staat, is de betreffende tabel alleen beschikbaar binnen de interne omgeving.
- **Vereis inlog voor deze dataset:** Wanneer "vereis inlog voor deze tabel" aan staat, is de betreffende tabel alleen beschikbaar voor personen die zijn ingelogd binnen de Atlas-omgeving.