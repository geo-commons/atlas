# Instructions to convert GeoTiff to GeoTiff with JPEG compression

1.
## A note on definitions

It&#39;s important to get the definitions straight as the nomenclature of file naming conventions can be confusing.

- **TIFF:** Tag Image File Format, a format for storing raster graphics images. The filename extension is: .tiffor .tif
- **GeoTIFF:** A public domain metadata standard which allows embedding georeferencing information in a TIFF file. Note, the filename extension is still .tiffor .tif.
- **JPEG:** A commonly used method of lossy compression for digital images. However, JPEG as an image file format is also used, generally with the filename extension .jpg, .jpeg. Thus, JPEG is both a file format as well as a method to compress images.

1.
## Instructions

Credits for the following instructions go to the Datalab of the Municipality of Purmerend.

A GitHub repository with the same instructions (Dutch) can be found at: [https://gitlab.com/purmerend/atlas/-/blob/master/docs/CREATE\_GEOTIFF\_WITH\_JPEG\_COMPRESSION.md](https://gitlab.com/purmerend/atlas/-/blob/master/docs/CREATE_GEOTIFF_WITH_JPEG_COMPRESSION.md)

Do keep in mind that the instructions in this GitHub has some minor, albeit crucial, syntax errors. These errors have been improved in the instructions below.

All image suppliers are expected to follow these steps for a uniform delivery of images for all municipalities. Logically, suppliers must use georeferenced .tif files in order to follow these steps.

  1.
## Software specifications

All described steps were executed using CentOS 7.4 (Linux), Pop!\_OS 20.10 (Linux), and OSX Catalina (MacOS).

For the JPEG compression of GeoTIFF files,[GDAL](https://gdal.org/) was used. For downloading instructions, follow the first link in the sources below.

  1.
## Mosaicking and compression instructions

The goal of these instructions is to change large GeoTIFF images into, smaller, compressed GeoTIFFs. This is done using JPEF a compression method.

Converting individual TIFF files to a TIFF mosaic compressed with JPEG happens in three steps:

1. **Virtually mosaicking different files into one.**

gdalbuildvrt -srcnodata &quot;255 255 255&quot; \&lt;output-file.tif\&gt; \&lt;input-files.tif\&gt;

**-srcnodata &quot;255 255 255&quot;** : make no data pixels white (as defined by the numbers). Other colours can also be selected, but white is deemed the most neutral for the viewer&#39;s experience.

**\&lt;output-file.tif\&gt;:** this is the name of the expected output file. E.g.: _output.tif_

**\&lt;input-files.tif\&gt;:** the name of the inputs. Here it&#39;s useful to use \*.tif in order to select **all**.tif files in the folder.

**General example of the code in practice** when running the command line from the folder where the files are located – notice that the &quot;\&lt; \&gt;&quot; are not actually in the line:

gdalbuildvrt -srcnodata &quot;255 255 255&quot; vrt\_output.tif \*.tif

1. **Converting a TIFF file to a TIFF with JPEG compression.**

gdal\_translate -a\_srs &quot;EPSG:28992&quot; -co &quot;COMPRESS=JPEG&quot; -co &quot;TILED=YES&quot; -co &quot;PHOTOMETRIC=YCBCR&quot; -co BIGTIFF=YES \&lt;input-file.tif\&gt; \&lt;output-file.tif\&gt;

**-a\_src &quot;EPSG&quot;** : assigns the projection. It seems that this is not correctly taken from the original GeoTiff files. Hence, one must assign it here.

**-co &quot;COMPRESS=JPEG&quot;:** Compression parameters are defined after **-co**. Here, JPEG compression is selected.

**-co &quot;TILED=YES&quot;:** Make it possible to tile the image so the viewer-application doesn&#39;t have to do this.

**-co &quot;PHOTOMETRIC=YCBCR&quot;:** JPEG compression works better within the YCBCR colour space.

**-co BIGTIFF=YES:** TIFF is a 32 bit format. As such, the output has a size limit of 4GB. To allow larger files to be created, this parameter is needed.

**\&lt;input-file.tif\&gt;:** the name of the input. This is the output of the first line. E.g. _vrt\_output.tif_

**\&lt;output-file.tif\&gt;:** this is the name of the expected output file. E.g.: _output\_compressed.tif_

**Note:** Although it&#39;s possible to change the compression factor with **-co JPEG\_QUALITY=XX** , where **XX** is the compression factor. This is not added to the line above as the standard compression factor of 75 is used.

**General example of the code in practice** when running the command line from the folder where the files are located:

gdal\_translate -a\_srs &quot;EPSG:28992&quot; -co &quot;COMPRESS=JPEG&quot; -co &quot;TILED=YES&quot; -co &quot;PHOTOMETRIC=YCBCR&quot; -co BIGTIFF=YES vrt\_output.tif output\_compressed.tif

1. **Building overview images within the GeoTIFF file. This is useful for quicker loading/displaying in web viewers.**

gdaladdo --config BIGGTIFF\_OVERVIEW YES --config COMPRESS\_OVERVIEW JPEG --config PHOTOMETRIC\_OVERVIEW YCBCR --config INTERLEAVE\_OVERVIEW PIXEL -r average \&lt;input-file.tif\&gt; 2 4 8 16

**--config BIGGTIFF\_OVERVIEW YES** : Not all parameters are the same across GDAL utilities. In this case, _BIGGTIFF\_OVERVIEW YES_ is the same as _BIGGTIFF = YES_.

**--config COMPRESS\_OVERVIEW JPEG** : The same as _COMPRESS=JPEG_.

**--config PHOTOMETRIC\_OVERVIEW YCBCR** : The same as _PHOTOMETRIC=YCBCR_.

**--config INTERLEAVE\_OVERVIEW PIXEL** : A choice can be made between _BAND_ and _PIXEl_. _PIXEL_ is needed in this case.

**-r average** : The resampling algorithm.

**\&lt;input-file.tif\&gt;:** the name of the input. This is the output of the second line. E.g_. compressed\_output.tif_

**2 4 8 16** : The overview levels.

**General example of the code in practice** when running the command line from the folder where the files are located:

gdaladdo --config BIGGTIFF\_OVERVIEW YES --config COMPRESS\_OVERVIEW JPEG --config PHOTOMETRIC\_OVERVIEW YCBCR --config INTERLEAVE\_OVERVIEW PIXEL -r average compressed\_output.tif 2 4 8 16

  1.
## Batch compression of individual GeoTIFF files (tested on Linux only)

In order to compress multiple GeoTIFFS without mosaicking them into a larger GeoTIFF, one must repeat the second step described above. This can be done by using the following line:

for f in \*.tif; do

gdal\_translate -a\_srs &quot;EPSG:28992&quot; -co &quot;COMPRESS=JPEG&quot; -co &quot;TILED=YES&quot; -co &quot;PHOTOMETRIC=YCBCR&quot; -co BIGTIFF=YES &quot;$f&quot; &quot;\&lt;output\_folder\&gt;/\&lt;possible\_prefix\&gt;$f&quot;

done

**\&lt;output\_folder\&gt;** : the folder name where you want the outputs to go. If the outputs have the same name as the inputs these cannot be saved in the same folder. As such, this parameter is needed.

**\&lt;possible\_prefix\&gt;** : in case a prefix is necessary, write it here. Follow the guidelines regarding the naming conventions.

**General example of the code in practice** when running the command line from the folder where the input files are located. In this case, the output folder is also found in the same folder where all the images are:

for f in \*.tif; do

gdal\_translate -a\_srs &quot;EPSG:28992&quot; -co &quot;COMPRESS=JPEG&quot; -co &quot;TILED=YES&quot; -co &quot;PHOTOMETRIC=YCBCR&quot; -co BIGTIFF=YES &quot;$f&quot; &quot;compressed\_outputs/compressed\_$f&quot;

done

1.
## Useful sources

[https://developers.planet.com/planetschool/getting-started-with-gdal/](https://developers.planet.com/planetschool/getting-started-with-gdal/)

[https://gdal.org/index.html](https://gdal.org/index.html)

[https://docs.geoserver.org](https://docs.geoserver.org/)

[https://www.geosolutionsgroup.com/technologies/geoserver/](https://www.geosolutionsgroup.com/technologies/geoserver/)

[https://docs.geoserver.geo-solutions.it/edu/en/enterprise/raster.html](https://docs.geoserver.geo-solutions.it/edu/en/enterprise/raster.html)

[http://blog.cleverelephant.ca/2015/02/geotiff-compression-for-dummies.html](http://blog.cleverelephant.ca/2015/02/geotiff-compression-for-dummies.html)

[https://docs.geoserver.org/latest/en/user/tutorials/imagepyramid/imagepyramid.html#building-and-using-an-image-pyramid](https://docs.geoserver.org/latest/en/user/tutorials/imagepyramid/imagepyramid.html#building-and-using-an-image-pyramid)

[https://github.com/planetfederal/workshops/blob/master/workshops/data\_configs/sphinx/source/raster.rst](https://github.com/planetfederal/workshops/blob/master/workshops/data_configs/sphinx/source/raster.rst)

[https://github.com/OSGeo/gdal/issues/1442](https://github.com/OSGeo/gdal/issues/1442)
