## FLAT model

***This file provides instructions on how to run the FLAT model.***

The Fine-Scale Land Allocation Tool (FLAT) is a statistical-based open access tool that combines dependent variable data measured at an aggregate level (e.g., state/provincial or national) with independent variable data measured at the pixel level to produce estimates of the dependent variable at the pixel level. Aggregate dependent variables can be land-use statistics at the regional level such as the total area of cropped land and the share of cropped land devoted to a particular crop. Pixel level independent variables can be basic biophysical land attributes. 

* Code: Available openly [here](https://mygeohub.org/resources/flat)

**Note!** that you will need [R](https://www.r-project.org/) installed in your local machine to execute the model. Also, for big datasets a **GAMS** licence is required. 

Once downloaded and installed, FLAT can be executed as follows:


##### Pipeline

**Step 1.** Checking status/preping

- Go to the model's root directory:

>/ FLAT_model/src

- There run:
>Rscript RforFLAT.R MOZ_points_010719.csv 0.534 1 15

where:
- RforFLAT.R is a script checking/preparing input dataset
- flat_input_Maize_10km.csv is the output csv of dowscaling_preping
- 0.534 is the target spatial resolution (1km) in arc.min
- 1 is the number of modelled crops (we only deal with one crop at the time)
- 15 is the number of independent variables (selected predictors)

**Note!** In this project we have slightly modified the RforFLAT.R code so as to meet the needs of our analysis. You can use the one available in the FLAT_model subfolder.

--------------------------------------------------------------------------------
**Step 2.** Running the model

- After running the R script, 9 csv files should have been created (cropnames, pixels, states, data, statelevelcroparea, name, 
pixelarea, statelevelareainfo, variables). 

- Copy above 9 files into:
>/ FLAT_model/src/resource (make sure that FLAT.gms is there)

- Open the GAMS Terminal and move to the (/FLAT_model/src/resource), there run:
>gams FLAT.gms

- At this point a licence will raise an error in the terminal if files are too big. In case valid licence exists, the FLAT.ist will be generated (log file) with results being available in a file called ```finalresults.dat```. Other output files include: 
- Pixel-level cropland predictions against FAO aggregate values
- Coefficient estimates
- Standard error
- Covariate matrix for parameter estimation

--------------------------------------------------------------------------------
**Step 3.** Transform result file into "right" format

- To generate a .tif raster, copy and paste finalresults.dat in the previous directory (```/FLAT_model/src```) and there run:
>/ Rscript dattotiff.R maize finalresults.dat

- Or you can run the ```Dat to csv.ipynb``` to convert and export results into a csv file that can be later used in the irrigation model. Output of this process should look like ```Sample_FLAT_output.csv.csv```.

--------------------------------------------------------------------------------

Once the input dataset is ready then we can move on preparing the input file for the agrodem model as described [here](https://github.com/akorkovelos/agrodem/blob/master/agrodem_preprocessing/Agrodem_Prepping.md).