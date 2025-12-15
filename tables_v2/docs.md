## Models

### TableTemp

Het `TableTemp` model representeert een tabel in Atlas die data kan ophalen van verschillende brontypes.

**Velden:**
- `title`: De naam van de tabel
- `slug`: Een uniek kort kenmerk voor de tabel (automatisch gegenereerd uit title)
- `source`: Een one-to-many relatie naar een Source object
- `source_type`: Het type bron (OWS, of REST)
- `fields`: JSON veld voor het opslaan van veldconfiguratie

**OWS Tables (source_type = 'OWS'):**

Voor OWS bronnen gebruik je CQL filters om data op te halen:

- `list_cql_filters`: JSON object met CQL filter waarden voor het ophalen van lijstweergaves
  ```json
  {
    "straatnaam": "{{straatnaam}}",
    "adres": "{{straatnaam}} {{huisnummer}}"
  }
  ```
  Elke key in het object representeert een filter naam, en de value is een CQL filter expressie met variabelen tussen `{{}}`.

- `detail_cql_filters`: JSON object met CQL filters voor het ophalen van details
  ```json
  {
    "straatnaam": "{{straatnaam}}",
    "adres": "{{straatnaam}} {{huisnummer}}",
    "staatId": "{{id}}"
  }
  ```
  
- `layer_name`: Laag naam van de laag op GeoServer

**REST Tables (source_type = 'REST'):**

Voor REST bronnen gebruik je endpoints met variabelen:

- `list_endpoint`: Het endpoint voor het ophalen van lijsten
  ```
  /zoeken/?straatnaam={{straatNaam}}&postCode={{postCode}}
  ```
  Variabelen worden tussen `{{}}` geplaatst en worden vervangen met werkelijke waarden.

- `detail_endpoint`: Het endpoint voor het ophalen van details
  ```
  /zoeken/?id={{id}}
  ```

**Relaties:**
- `related_tables`: ManyToMany relatie met andere TableTemp objecten via de TableToTable through table

### TableToTable

Het `TableToTable` model definieert de relatie tussen twee tabellen en hoe hun velden op elkaar worden gemapt.

**Velden:**
- `from_table`: De brontabel (ForeignKey naar TableTemp)
- `to_table`: De doeltabel (ForeignKey naar TableTemp)
- `field_mapping`: JSON object dat aangeeft welke velden van de brontabel naar welke velden van de doeltabel worden gemapt

**Voorbeeld field_mapping:**
```json
{
  "ligplaatsnummer": "ligplaatsnummer2",
  "straatnaam": "straat"
}
```

De keys zijn veldnamen in de `from_table`, en de values zijn veldnamen in de `to_table`.

**Constraints:**
- `unique_together`: Een combinatie van from_table en to_table moet uniek zijn

### LayerToTable

Het `LayerToTable` model definieert de relatie tussen een Layer en een Table, en hoe hun velden op elkaar worden gemapt.

**Velden:**
- `from_layer`: De bronlaag (ForeignKey naar Layer)
- `to_table`: De doeltabel (ForeignKey naar TableTemp)
- `field_mapping`: JSON object dat aangeeft welke velden van de layer naar welke velden van de tabel worden gemapt

**Voorbeeld field_mapping:**
```json
{
  "ligplaatsnummer": "ligplaatsnummer2",
  "objectId": "id"
}
```

De keys zijn veldnamen in de `from_layer`, en de values zijn veldnamen in de `to_table`.

**Constraints:**
- `unique_together`: Een combinatie van from_layer en to_table moet uniek zijn
