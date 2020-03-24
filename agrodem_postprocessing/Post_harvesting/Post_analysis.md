## Post analysis

***Post analysis of the agrodem resuls***

##### Input files

* agrodem results ```Sample_Moz_Maize_2017_1km_Results.csv```
* Administrative layer boundaries (level 2)

**Note!** ```Sample_Moz_Maize_2017_1km_Results.csv``` shows only areas in need for irrigation, not all areas where the crop is cultivated. In case a user want the latter, ```agrodem.ipynb``` saving file options shall be modified accordingly (code already there; it needs to be un-commented)

Code: ```Result_post_analysis.ipynb```

##### Output

The code produces detailed and/or aggregate (amdinistrative) maps of electricity requirements for irrigation and post-harvesting activities of the crop modelled over the area of interest.