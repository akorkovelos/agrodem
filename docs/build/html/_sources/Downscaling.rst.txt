Downscaling
=================================

Overview
****************
High resolution crop allocation datasets are not usually available in open access sources. ‘Downscaling models’ for land cover use high-resolution biophysical data (e.g. on temperature, precipitation and/or soil pH) which have predictive power over low-resolution input data (e.g. national or admin level aggregate values of harvested area, production etc.). 

In order to do so, we have used the `Fine Scale Land Allocation Tool or FLAT <https://mygeohub.org/resources/flat>`_ model.  FLAT is a statistical-based open access tool that combines dependent variable data measured at an aggregate level (e.g., state/provincial or national) with independent variable data measured at the pixel level to produce estimates of the dependent variable at the pixel level. 


Input data preparation
************************

In terms of the crop harvested area, harvested land shares of e.g. maize were extracted from the `FAO Agro MAPS Global Spatial Database of Agricultural Land use Statistics <http://www.fao.org/land-water/land/land-governance/land-resources-planning-toolbox/category/details/en/c/1026341/>`_. The database provides agricultural statistics and data collected and compiled from national resources, surveys, and official in-country agencies, assuring some degree of consistency across different agricultural products and geographic areas. This consistency is considered highly important in this developed modelling approach, making it easier replicable and further applied to other regions or agricultural products by avoiding highly processed or already disaggregated input data which might be based on ad hoc assumptions or poorly documented methodological steps. 

For the purposes of this study level 2 administrative crop data were used as shown in Figure below.

.. figure::  images/Downscaling_Fig.jpg
   :align:   center

   Visualisation of harvested area data of rainfed maize in Mozambique as retrieved from FAO Agro-Maps

.. note::
   In case input data is outdated, they will need to be projected to the base year. For example in this case the total harvested area for maize was equal to only 782,608 ha in 2008 (input data), while 2017-18 FAO estimates indicate about 1,962,000 ha in Mozambique. This is included in a python script available as `Preparing Agro Maps <https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Downscaling/Downscaling_prepping/Preparing_Agro_Maps.ipynb>`_.

Then, the above dataset is transformed into a base (vector) layer at the targeted downscaling resolution. This is used later on to extract the predictor attributes per location. The steps for this are as follows:

1. Project crop layer to target crs (in this case EPSG: 32737 – WGS 84/UTM zone 37S ) 
2.	Calculate “area” in sq.km and “perimeter” in km for listed admin areas
3.	Convert “area” from sq.km to ha
4.	Create the base grid mesh (10km, 5km, 1km, 500m or 250m)  
5.	Only keep locations where harvested area for the listed crop is available.
6.	Convert polygons to centroids indicating the location of crops at the selected resolution.
7.	Export output as a .csv file 

.. note::
	In order to facilitate the process, we have developed a `QGIS plugin <https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Downscaling/Downscaling_prepping/Agrodem_plugin_creating_basegrid-master.zip>`_ that together with instructions for installationa dn use is available online. 

Finally, once base (vector) data layer is ready and available as a .csv file, predictor values are attributed. As predictors in the FLAT model, we may use the following 15 variables:

* Average temperature 
* Average solar irradiation 
* Average precipitation  
* Average wind speed
* Soil Ph in H20
* Depth to bedrock
* Bulk density
* lay content
* Texture class
* Soil organic carbon
* Drainage class
* EVI
* NDVI
* Elevation - Slope
* Cropland extent

.. note::
	All of the above data can be collected either in their raw format or using a Python script (`GEE_Imagery_Extraction <https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Downscaling/Downscaling_prepping/GEE_Imagery_Extraction.ipynb>`_) that was developed specifically for the extraction of the Images and ImageCollections using the GEE API. 

.. note::
	In order to automate the attribute extraction process, a Python script (`FLAT prepping <https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Downscaling/Downscaling_prepping/FLAT%20prepping.ipynb>`_) was developed for further processing of all geospatial data, and an aggregated final .csv table was extracted as the final input to the econometric model. Data processing included:

	* data cleaning
	* transformation and integration from the different sources
	* accounting for missing and extreme values (null or corrupted)
	* variable name inconsistencies
	* variable type conversions, scaling and data normalization 

	With regards to the imported geospatial layers – raster (.tiff) and vector (.shp) files – each dataset is expressed and stored as a single vertical layer in the same coordinate system e.g. EPSG: 32737 – WGS 84/UTM zone 37S (+proj=utm +zone=37 +south +datum=WGS84 +units=m +no_defs for Mozambique). 

.. figure::  images/Downscaling_Fig2.jpg
   :align:   center

   Snapshot of the .csv file used as input to the FLAT model

Parameterization & model run
******************************

The FLAT model can be executed with the following steps.

**Step 1.**	Go to directory:
					
					>/ FLAT_model/src

**Step 2.**	In the directory run:
					
					>/ Rscript RforFLAT.R flat_input.csv 0.534 1 15

					where:

					* flat_input.csv is the output csv of FLAT prepping process 
					* 0.534 is the target spatial resolution in arc.min
					* 1 is the number of modelled crops 
					* 15 is the number of independent variables

.. note::
	This process requires `R <https://www.r-project.org/>`_ to be installed at your working station. Running the above script creates nine derivative .csv files that the FLAT model requires to run. These are usually named as cropnames, pixels, states, data, statelevelcroparea, name, pixelarea, statelevelareainfo and variables. 

**Step 3.**	Copy the nine .csv files into the resource directory:
					
					>/ FLAT_model/src/resource

.. note::
	FLAT.gms should be located in the same directory as well - default by installation.

**Step 4.**	Open GAMS Terminal; move to resource directory and run:

					>/ gams FLAT.gms

.. note::
	This will run FLAT model. Once complete, the log file (FLAT.ist) will be generated. This can be used to monitor the specifics of the run and track any issue in the debugging process (if needed). The result file is a .dat file usually under the name “finalresults.dat”. Other output files might include “Pixel-level cropland predictions against FAO aggregate values”; “Coefficient estimates”; ”Standard error”; “Covariate matrix for parameter estimation”.

**Step 5.**	Export results (Optional) 

					>/ FLAT_model/src

					run > Rscript dattotiff.R maize finalresults.dat (to generate a raster file (.tiff) of the results) or 

					run > Result.r (to export results in .csv format)

.. note::
	Transformation of the result (.dat) file into a .csv file that can later on be used for the irrigation model is also available in `Dat to csv <https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Downscaling/FLAT_model/finalresults.dat>`_.


Output data
****************
The output file provides a prediction the downscaled crop allocation. Each location (point in the vector layer) is attributed a fraction of the total harvested areas of the initial value (this refers to the admin level 2 value in this case). Aggregation of the downscaled results sum up to the original values. 

.. figure::  images/Downscaling_Fig3.jpg
   :align:   center

   Example output from the downscaling process for rainfed maize in Mozambique

Special notes
****************
The downscaling process is a good – yet experimental – way to achieve higher granularity of crop distribution, especially in areas where there is data scarcity. 

The FLAT model that was selected in this assignment is open source (although GAMS is needed for big datasets) and straightforward to test, use and customize. It predicts cropland allocation using pixel-level biophysical attributes which are openly available at the desired spatial resolution (1 km). The econometric approach provides estimates of the effects of biophysical factors on cropland allocation. 

FLAT performance metrics are in alignment with available literature; visual inspection of results does also agree with qualitative findings from sample agricultural survey. However, the selected cross-validation approach highlighted that inconsistencies in the sample dataset are high to achieve any satisfactory results. This highlights the need for standardization of collection, processing and dissemination of survey related datasets.

.. note::
	A first and second order validation process was conducted in this project and is available in the `project report <tbd>`_. This was implemented through a Python script available as `CrossValidation <https://github.com/akorkovelos/agrodem/tree/master/agrodem_postprocessing/Cross_Validation>`_. 