## agrodem prepping

***This file provides instructions on how to prepare the crop input file (e.g. ```Pilot_Moz_Maize_Sample_1km.csv```) for the agrodem model.***

##### Input

The point of departure is a vector dataset (in csv format) that contains potential nodes for irrigation. Each feature should be attributed with:

1. unique index 
2. state name
3. lon/lat (in deg WGS84)
4. crop name 
5. harvested area in hectares (ha)

See for example ```Sample_input.csv```

The ```Sample_input.csv``` represents location of crop fields and can be used at any available spatial esolution. It can for example be simply 10x10km data from [Harvest Choice](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PRFF8V) or the output of a more detailed downscaling method (see relevant sub-folder).

**Note!** The "fraction" column (in the example above) is only a remnant of the downscaling process (explained on relevant sub-folder) and not essential in this step.

##### Pipeline

There are two main steps that are required explained below:

- **Step 1** - Extracting atributes related to surface water availability (sw_dist, sw_depth, sw_suit_idx). For this, we have developed a Qgis plugin (```Surface Water Extractor```), which is available in a separate sub-folder together with installation and use instructions.

See example output of step 1 in ```Sample_output (step 1).csv```

--------------------------------------------------------------------------------

- **Step 2** - Extracting all the other necessary attributes as described in **agrodem.ipynb**. For this, we have developed the ```Agrodem_Prepping.ipynb```, which takes the result from step 1 and conducts an extraction analysis with the use of spatial packages and Qgis. 

This step requires acquisition of the following raster datasets:

* elevation (in m)
* gw_depth (Ground water depth in m)
* awsc (Water storage capacity of the soil in mm/m)
* prec_i (Average precipitation in mm/month; i=1-12)
* srad_i (Average solar irradiation per month in kJ m-2 day-1; i=1-12)
* wind_i (Average wind speed per month in m s-1; i=1-12)
* tavg_i, tmax_i, tmin_i (Average, Max, Min temperature per month in C; i=1-12)

See example output of step 2 in ```Sample_output (step 2).csv```

**Note!** These, cannot be stored in this repo due to size limitations. They are however openly available online (for more info see [project's documentation](https://agrodem.readthedocs.io/en/latest/index.html). Access to the project's dedicated S3 database can be granted upon request. 

##### Output

The result of steps 1 & 2 should be similar to the ```Pilot_Moz_Maize_Sample_1km.csv```