# 1. A note on definitions

It's important to get the definitions straight as the nomenclature of
file naming conventions can be confusing.

-   **TIFF:** Tag Image File Format, a format for storing raster
    graphics images. The filename extension is: .tiff or .tif

-   **GeoTIFF:** A public domain metadata standard which allows
    embedding georeferencing information in a TIFF file. Note, the
    filename extension is still .tiff or .tif.

-   **JPEG:** A commonly used method of lossy compression for digital
    images. However, JPEG as an image file format is also used,
    generally with the filename extension .jpg, .jpeg. Thus, JPEG is
    both a file format as well as a method to compress images.

# 2. Instructions

Credits for the following instructions go to the Datalab of the
Municipality of Purmerend.

A GitHub repository with the same instructions (Dutch) can be found at:
<https://gitlab.com/purmerend/atlas/-/blob/master/docs/CREATE_GEOTIFF_WITH_JPEG_COMPRESSION.md>

Do keep in mind that the instructions in this GitHub has some minor,
albeit crucial, syntax errors. These errors have been improved in the
instructions below.

All image suppliers are expected to follow these steps for a uniform
delivery of images for all municipalities. Logically, suppliers must use
georeferenced .tif files in order to follow these steps.

## 2.1 Software specifications

All described steps were executed using CentOS 7.4 (Linux), Pop!\_OS
20.10 (Linux), and OSX Catalina (MacOS).

For the JPEG compression of GeoTIFF files, [GDAL](https://gdal.org/) was
used. For downloading instructions, follow the first link in the sources
below.

## 2.2 Mosaicking and compression instructions

The goal of these instructions is to change large GeoTIFF images into,
smaller, compressed GeoTIFFs. This is done using JPEF a compression
method.

Converting individual TIFF files to a TIFF mosaic compressed with JPEG
happens in three steps:

  **1. Virtually mosaicking different files into one.**

> gdalbuildvrt -srcnodata \"255 255 255\" \<output-file.tif\>
> \<input-files.tif\>

**-srcnodata "255 255 255"**: make no data pixels white (as defined by
the numbers). Other colours can also be selected, but white is deemed
the most neutral for the viewer's experience.

**\<output-file.tif\>:** this is the name of the expected output file.
E.g.: *output.tif*

**\<input-files.tif\>:** the name of the inputs. Here it's useful to use
\*.tif in order to select **all** .tif files in the folder.

> **General example of the code in practice** when running the command
> line from the folder where the files are located -- notice that the
> "\< \>" are not actually in the line:
>
> gdalbuildvrt -srcnodata "255 255 255" vrt_output.tif \*.tif

**2. Converting a TIFF file to a TIFF with JPEG compression.**

>gdal_translate -a_srs "EPSG:28992" -co "COMPRESS=JPEG" -co "TILED=YES"
>-co "PHOTOMETRIC=YCBCR" -co BIGTIFF=YES \<input-file.tif\>
>\<output-file.tif\>

**-a_src "EPSG"**: assigns the projection. It seems that this is not
correctly taken from the original GeoTiff files. Hence, one must assign
it here.

**-co "COMPRESS=JPEG":** Compression parameters are defined after
**-co**. Here, JPEG compression is selected.

**-co "TILED=YES":** Make it possible to tile the image so the
viewer-application doesn't have to do this.

**-co "PHOTOMETRIC=YCBCR":** JPEG compression works better within the
YCBCR colour space.

**-co BIGTIFF=YES:** TIFF is a 32 bit format. As such, the output has a
size limit of 4GB. To allow larger files to be created, this parameter
is needed.

**\<input-file.tif\>:** the name of the input. This is the output of the
first line. E.g. *vrt_output.tif*

**\<output-file.tif\>:** this is the name of the expected output file.
E.g.: *output_compressed.tif*

**Note:** Although it's possible to change the compression factor
with **-co JPEG_QUALITY=XX**, where **XX** is the compression factor.
This is not added to the line above as the standard compression factor
of 75 is used.

> **General example of the code in practice** when running the command
> line from the folder where the files are located:
>
> gdal_translate -a_srs "EPSG:28992" -co "COMPRESS=JPEG" -co "TILED=YES"
> -co "PHOTOMETRIC=YCBCR" -co BIGTIFF=YES vrt_output.tif
> output_compressed.tif

  **3. Building overview images within the GeoTIFF file. This is useful for quicker loading/displaying in web viewers.**

> gdaladdo \--config BIGGTIFF_OVERVIEW YES \--config COMPRESS_OVERVIEW
> JPEG \--config PHOTOMETRIC_OVERVIEW YCBCR \--config INTERLEAVE_OVERVIEW
> PIXEL -r average \<input-file.tif\> 2 4 8 16

**\--config BIGGTIFF_OVERVIEW YES**: Not all parameters are the same
across GDAL utilities. In this case, *BIGGTIFF_OVERVIEW YES* is the same
as *BIGGTIFF = YES*.

**\--config COMPRESS_OVERVIEW JPEG**: The same as *COMPRESS=JPEG*.

**\--config PHOTOMETRIC_OVERVIEW YCBCR**: The same as
*PHOTOMETRIC=YCBCR*.

**\--config INTERLEAVE_OVERVIEW PIXEL**: A choice can be made between
*BAND* and *PIXEl*. *PIXEL* is needed in this case.

**-r average**: The resampling algorithm.

**\<input-file.tif\>:** the name of the input. This is the output of the
second line. E.g*. compressed_output.tif*

**2 4 8 16**: The overview levels.

> **General example of the code in practice** when running the command
> line from the folder where the files are located:
>
> gdaladdo \--config BIGGTIFF_OVERVIEW YES \--config COMPRESS_OVERVIEW
> JPEG \--config PHOTOMETRIC_OVERVIEW YCBCR \--config
> INTERLEAVE_OVERVIEW PIXEL -r average compressed_output.tif 2 4 8 16

## 2.3 Batch compression of individual GeoTIFF files (tested on Linux only)

In order to compress multiple GeoTIFFS without mosaicking them into a
larger GeoTIFF, one must repeat the second step described above. This
can be done by using the following line:

> for f in \*.tif; do
> 
> gdal_translate -a_srs "EPSG:28992" -co "COMPRESS=JPEG" -co "TILED=YES"
> -co "PHOTOMETRIC=YCBCR" -co BIGTIFF=YES "\$f"
> "\<output_folder\>/\<possible_prefix\>\$f"
> 
> done

**\<output_folder\>**: the folder name where you want the outputs to go.
If the outputs have the same name as the inputs these cannot be saved in
the same folder. As such, this parameter is needed.

**\<possible_prefix\>**: in case a prefix is necessary, write it here.
Follow the guidelines regarding the naming conventions.

> **General example of the code in practice** when running the command
> line from the folder where the input files are located. In this case,
> the output folder is also found in the same folder where all the
> images are:
>
> for f in \*.tif; do
>
> gdal_translate -a_srs "EPSG:28992" -co "COMPRESS=JPEG" -co "TILED=YES"
> -co "PHOTOMETRIC=YCBCR" -co BIGTIFF=YES "\$f"
> "compressed_outputs/compressed\_\$f"
>
> done

# 3. Useful sources

<https://developers.planet.com/planetschool/getting-started-with-gdal/>

<https://gdal.org/index.html>

<https://docs.geoserver.org>

<https://www.geosolutionsgroup.com/technologies/geoserver/>

<https://docs.geoserver.geo-solutions.it/edu/en/enterprise/raster.html>

<http://blog.cleverelephant.ca/2015/02/geotiff-compression-for-dummies.html>

<https://docs.geoserver.org/latest/en/user/tutorials/imagepyramid/imagepyramid.html#building-and-using-an-image-pyramid>

<https://github.com/planetfederal/workshops/blob/master/workshops/data_configs/sphinx/source/raster.rst>

<https://github.com/OSGeo/gdal/issues/1442>
