Via de beheerpagina kom je bij de verschillende onderdelen die ingesteld kunnen worden.

<img src="../images/beheerpagina.png" alt="Hoofdscherm Admin module" width="700"/>

###Importeren en Exporteren van configuratiegegevens.

<img src="../images/acties.png" alt="Importeren en Exporteren" width="300"/>

Voor backup-doeleinden en het up-to-date houden van een testomgeving, is het mogelijk bij bepaalde onderdelen om de gegevens te exporteren en te importeren. Dit geldt voor de onderdelen bij Kaarten, Gebruikersbeheer, autorisaties onder Autorisatie en Tabellen onder Tabellen. Let op dat bij de laatste alleen de definitie van de tabellen wordt geëxporteerd, niet de inhoud. De gegevens van een export worden opgeslagen als JSON bestand. Houd er rekening mee dat ontbrekende gegevens in een ander onderdeel niet automatisch worden aangemaakt bij een gedeeltelijke import. Bijvoorbeeld: wanneer een export van Kaarten wordt geïmporteerd maar de kaartlagen die daarbij horen ontbreken in het onderdeel Kaartlagen, dan zal zo'n kaart niet werken. Alle onderliggende data moet overgezet worden.

<!-- [Volgende](kaarten.md){ .md-button } -->
