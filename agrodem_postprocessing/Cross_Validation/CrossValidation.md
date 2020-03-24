## Cross-validation of downscaled data

***This file provides a brief description of the cross-validation process between downscaled crop data and sample survey data***

##### Input files

* Downscaled crop data ```Maize_Moz_1km_2017_downscaled.csv```
* Survey data ```Survey_Points_Maize_epsg_4326.csv``` 
* Administrative layer boundaries (level 2)

**Note!** Input datasets are available in [input_data sub-folder](https://github.com/akorkovelos/agrodem/tree/master/agrodem_postprocessing/Cross_Validation/Input_data). Also, conversion of the survey data to .csv format can be done using ```Processing Sample data from R.ipynb```.

##### Process

There are 28158 points in the survey. ```Cross-validation of FLAT output.ipynb``` elaborates on two methods of cross-validation.

**Method A.** Uses spatial intersection for all survey locations within 500m from a downscaled point. Survey data are then aggregated and compared (in correlation graphs) with corresponding downscaled value of harvested area.

**Method B.** Spatial statistics are used in order to examine "binary" correlation (based on confusion matrix) between the two datasets. That is, whether survey data locations are in close proxility to the "predicted" downscaled crop locations. 