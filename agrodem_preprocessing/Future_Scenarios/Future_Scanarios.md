## Future scenarios

***This file provides instructions on how to prepare crop input files representing future scenarios.***

Scenarios can be generated in the following steps.


##### Extensification

**Step 1.** Find potential location for crop extension

This step take into account a numner of input layer, key parameters and modelling assumptions and provides the coordinates of potential future locations of the modelled crop (in raster format).

* Code: ```Making Future Scenarios.ipynb```

*Note!* The output of the code above is a raster (.tiff) dataset. Following to ```Step 2``` require the conversion to a vector layer. This can be done with the following code.

* Code: ```Converting raster to vector.ipynb```

**Note!** Input datasets cannot be stored in this repo due to size limitations. They are however openly available online (for more info see [project's documentation](https://agrodem.readthedocs.io/en/latest/index.html). Access to the project's dedicated S3 database can be granted upon request. 

--------------------------------------------------------------------------------

**Step 2.** Merge current and future crop extension

This step merges current crop extend with future crop allocation and creates an expected crop allocation file to be used (after prepped) to the irrigation model.

* Code: ```Processing_Future_Scen.ipynb```

##### Sensitivity

Another way to create new scenarios is by changing attributes of the crop input file (```Pilot_Moz_Maize_Sample_1km.csv```). This can help conduct a simple sensitivity analysis without re-collecting raw GIS input datasets (e.g. precipitation data). This can be done with the following code.


* Code: ```Changing Climatic Conditions.ipynb``` 

--------------------------------------------------------------------------------
Once the input dataset is ready then we can move on preparing the input file for the agrodem model as described [here](https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Agrodem_Prepping.md).