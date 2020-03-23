## Downscaling

***This file provides instructions on how to prepare a "downscaled" crop input file for the agrodem model.***

The downscaling process may be used to fill the gap in high resolution crop distribution data. Note that at the time of development the best available crop distribution datasets were available from [Harvest Choice](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PRFF8V), in coarse spatial resolution of (10x10 km). For downscaling we have decided to use the the open-source econometric model [FLAT](https://mygeohub.org/resources/flat) for cropland disaggregation (Song et al., 2018). The following 4 steps describe the process required to prepare the input data file for FLAT.


##### Pipeline

**Step 1.** Creating crop maps using tabular data on harvested area

This assumes that raw data are only avilabla in tabular format (see for example ```moz_all_data.csv```. Together with admin data (see ```gadm36_MOZ_2.shp``` they are used to create raster file outputs of crop distribution per admin level 2. 

* Code: ```Preparing_Agro_Maps.ipynb```
* Sample output: ```Moz_Maize_2000_admin2.shp```

--------------------------------------------------------------------------------
**Step 2.** Creating a grid-base-map of desired output spatial resolution

For this step we have developed a Qgis plugin which takes into account admin boundaries for the area or interest and the output of ```Step 1```. The module splits the initial low granularity map to the desired output spatial resolution (e.g. 10km, 5km, 1km, 500m) and generates an output csv file with coordinates of expected downscaled grid cells. 

* Code: ```Agrodem_plugin_creating_basegrid-master.zip``` 
* Sample output: ```Moz_Maize_2000_admin2_10km.csv```

**Note!** installation & use instructions for the plugin are available in the zipped folder.

--------------------------------------------------------------------------------

**Step 3.** Collect raw "predictor" datasets

Once the base map is ready (```Step 2```) then it should be attributed predictor values. In this example, we have decided to use 15 predictors including: 

1. Average temperature 
2. Average solar irradiation 
3. Average precipitation 
4. Average wind speed
5. Soil Ph in H20
6. Depth to bedrock
7. Bulk density
8. Clay content
9. Texture class
10. Soil organic carbon
11. Drainage class
12. EVI
13. NDVI
14. Elevation
15. Slope

Those were collected from **Google Earth Engine (GEE)** and clipped/processed for the use in our modelling exercise. This is a common statial practice and can be done in multiple ways; we have developed a jupyter notebook however each user can acquire the data as suitable per experience. 

* Code: ```GEE_Imagery_Extraction.ipynb``` 

**Note!** These, cannot be stored in this repo due to size limitations. They are however openly available online (for more info see [project's documentation](https://agrodem.readthedocs.io/en/latest/index.html). Access to the project's dedicated S3 database can be granted upon request. 

--------------------------------------------------------------------------------

**Step 4.** Extract predictor values to grid-base-map features

In this step the grid-base map (for a certain crop) is attributed with the predictor data. 

* Code: ```FLAT prepping.ipynb``` 
* Sample output: ```flat_input_Maize_10km.csv```
--------------------------------------------------------------------------------
Once the input dataset is ready then we can move in running the FLAT model. Proceed with running the FLAT model [here](https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Downscaling/FLAT_model/FLAT_model.md).