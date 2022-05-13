# Luchtfoto’s in ESRI GeoTiff mosaic formaat omzetten naar GeoTiff formaat met JPEG compressie.
  
Voor het weergeven en opslaan van geogerefereerde luchtfoto's zijn over het algemeen twee bestandsindelingen in gebruik: het <a href="https://nl.wikipedia.org/wiki/Tagged_image_file_format">TIFF</a> formaat en het <a  href="https://www.hexagongeospatial.com/en/products/power-portfolio/compression#gwc-webadmin-defaults">ECW</a> formaat. Het TIFF formaat is van zichzelf een 'losless' formaat en heeft als voordeel dat het een hoge beeldkwaliteit geeft. Het nadeel is dat de bestandsomvang erg groot is. ECW is een compressieformaat dat een kleinere bestandsomvang geeft en toch een hoge beeldkwaliteit. Toch zijn ECW bestanden nog relatief groot en bovendien is het gebruik van ECW <a href="https://community.hexagongeospatial.com/t5/APOLLO-ECW-Q-A/License-for-reading-or-writing-ECW-in-third-party-software/ta-p/34074"> gelicenseerd</a>.

Samen met partner <a href="https://www.delta10.nl">Delta10</a> heeft gemeente Purmerend gezocht naar een manier om de luchtfoto's naar een open formaat te converteren dat eenzelfde kwaliteit geeft als ECW en ook een kleinere bestandsomvang. Uiteindelijk zijn alle gemeentelijke luchtfoto's omgezet naar [TIFF formaat met JPEG compressie](#tiff_met_jpeg_compressie). Dit geeft een bestandsomvang die twee tot drie keer zo klein is als ECW maar wel dezelfde beeldkwaliteit heeft. 

Voor het omzetten is er uitgegaan van de aangeleverde Geotiff mosaic tegels. Deze zijn immers niet gecomprimeerd en geven dus de hoogste beeldkwaliteit bij de start.
Voor het omzetten van (<a href="https://www.esri.nl">ESRI</a>) Geotiff bestanden naar  [standaard Geotiff formaat](#standaard_geotiff_formaat) met JPEG compressie is gebruik gemaakt van [GDAL](https://gdal.org/) tools.

Onderstaande conversiestappen zijn uitgevoerd onder Centos 7.4 en OSX Catalina. Met de Windows versie van GDAL blijkt de conversie ook succesvol. De verschillende stappen worden vanaf de commandprompt uitgevoerd. Aangezien [QGIS](https://www.qgis.org) ook gebruik maakt van GDAL, kan de conversie ook daar uitgevoerd worden, dit valt buiten de scope van dit document.

  Het converteren van de mosaic bestanden kan in drie stappen gedaan worden:

1. Het virtueel samenvoegen van mosaic bestanden tot één bestand

2. Het converteren van TIFF naar een TIFF/JPEG bestand

3. Extra overview afbeeldingen maken binnen het GeoTiff bestand

  [**Gdallbuildvrt**](https://gdal.org/programs/gdalbuildvrt.html)

maakt een virtueel raster bestand aan. Een VRT bestand is een XML bestand met de informatie over de bronbestanden:

```bash
  gdalbuildvrt  -srcnodata "255 255 255" <output-bestand>  <input-bestanden bv.:  ../1_mosaic_tiles_TIFF_TFW/*.tif>
```

  [**Gdal_translate**](https://gdal.org/programs/gdal_translate.html)

zorgt voor de conversie tussen formaten

```bash
  gdal_translate -a_srs "PSG:28992" -co "COMPRESS=JPEG" -co "TILED=YES" -co "PHOTOMETRIC=YCBCR" -co BIGTIFF=YES <input-bestand.tif> <output-bestand.tif>
```

  [**Gdaladdo**](https://gdal.org/programs/gdaladdo.html)

voegt overzichten toe.

```bash
gdaladdo --config BIGGTIFF_OVERVIEW YES --config COMPRESS_OVERVIEW JPEG --config PHOTOMETRIC_OVERVIEW YCBCR --config INTERLEAVE_OVERVIEW PIXEL -r average <input-bestand.tif> 2 4 8 16 32
```

Afhankelijk van de grootte van de originele luchtfoto (de grootte van het grondgebied) en de gebruikte hardware, kan gdalladdo een half uur tot een hele dag of langer bezig zijn.
Het Geotiff bestand dat gdaladdo genereert kan als zodanig worden ingelezen in bijvoorbeeld [Geoserver](#http://geoserver.org)

Met [**gdalinfo**](https://gdal.org/programs/gdalinfo.html) kan het gegenereerde bestand bekeken worden. Wordt het juiste formaat gezien? Klopt de opgegeven projectie? etc.

Geraadpleegde sites:
- https://gdal.org/index.html
- https://docs.geoserver.org
- https://www.geosolutionsgroup.com/technologies/geoserver/
- https://docs.geoserver.geo-solutions.it/edu/en/enterprise/raster.html
- http://blog.cleverelephant.ca/2015/02/geotiff-compression-for-dummies.html
- https://docs.geoserver.org/latest/en/user/tutorials/imagepyramid/imagepyramid.html#building-and-using-an-image-pyramid
- https://github.com/planetfederal/workshops/blob/master/workshops/data_configs/sphinx/source/raster.rst
- https://github.com/OSGeo/gdal/issues/1442

---


#### STANDAARD_GEOTIFF_FORMAAT 
In een GeoTiff formaat bestand is grafische en geografische informatie opgeslagen in één bestand. Binnen de (sub) standaard van softwarefabrikant ESRI is de geografische informatie echter opslagen in een apart bestand. Deze zogenaamde [WorldFiles](https://en.wikipedia.org/wiki/World_file) krijgen bij Tiff bestanden de extensie TFW. Niet alle applicaties kunnen omgaan met losse TFW bestanden.

#### TIFF_MET_JPEG_COMPRESSIE
Het [TIFF](https://nl.wikipedia.org/wiki/Tagged_image_file_format) formaat is een container formaat. Dat wil zeggen dat binnen een TIFF bestand verschillende compressiemethoden mogelijk zijn, JPEG is er daar één van.

#### SRCNODATA
In tegenstelling tot veel andere bestandsformaten ondersteund JPEG geen transparantie. De achtergrond (nodata area) van een luchtfoto zal wit of zwart zijn (of elke andere kleur) in plaats van transparant. Door de compressie van JPEG is er geen duidelijk onderscheid tussen data en nodata. Hierdoor kunnen er artefacten ontstaan aan de data-randen die als zwarte of witte lijntjes te zien kunnen zijn. GDAL maakt bij JPEG compressie standaard een zwarte achtergrond. Door de parameter '-srcnodata 255 255 255' te gebruiken, wordt een witte achtergrond aangemaakt. Dit valt minder op dan zwart.
Uiteraard kan in plaats van 255 255 255 elke andere kleur gekozen worden.

#### GDAL_TRANSLATE
**-a_src “EPSG”**  geeft de gebruikte projectie aan. Het blijkt dat deze niet of niet goed wordt overgenomen uit de ESRI GeoTiff bestanden.

**-co “COMPRESS=JPEG”** Compressie opties worden genoteerd na de parameter -co. Er zijn meerdere mogelijk. Hier wordt de compressie ingesteld op JPEG.

**-co “TILED=YES”** Maak reeds in het output bestand tegels aan zodat de viewer-applicatiie dit niet hoeft te doen.

**-co "PHOTOMETRIC=YCBCR"** [Het JPEG algoritme werkt beter binnen de YCBCR kleur-ruimte](http://blog.cleverelephant.ca/2015/02/geotiff-compression-for-dummies.html)

**-co BIGTIFF=YES Tiff** is een 32 bits formaat. Daarom heeft het een grens van 4GB. Zijn (output) bestanden groter dan 4GB dan is deze optie nodig, anders stopt de conversie als het output bestand groter wordt dan 4GB.
