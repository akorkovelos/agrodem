# agrodem prepping

Code and scripts in this sub-folder aim to bring input data in appropriate form for the agrodem model to work as intended. 
That is, in the right format and with the right attrobutes as shown in the "agrodem_sample_input_data" folder in the root
directory.

The point of departure here is a vector dataset (in csv format) that contains 
a)unique index, 
b)state name, 
c)lon/lat (in deg WGS84), 
d)crop name 
e)harvested area in hectares (ha). 

See for example "Sample_input.csv". 

Note that fraction column is not necessary and is only a remnant of the downscaling process 
(explained on relevant sub-folder).

The "Sample_input.csv" represents location of crop fields and can be used at any available spatial esolution. It can for 
example be simply 10x10 km data from Harvest Choice or the output of a more detailed downscaling method (see relevant 
sub-folder).

There are two main processes that are required explained below:

- Process 1 - Extracting information regarding surface water availability
For this, we have developed a Qgis plugin. Instructions for installation and usage are available in the zipped folder.


- Process 2 - Extracting all necessary attributes as described in the first step of "agrodem.ipynb".
For this, we have developed the "Agrodem_Prepping.ipynb" which takes the result from process 1 (see "Sample_process1_output.csv")
and conducts an extraction analysis with the use of spatial packages and Qgis. Note that all raster datasets that are 
necessary for the module to run are available on the project's dedicated S3 database.

If sucessful, the result of process 1 & 2 should be similar to the "Pilot_Moz_Maize_Sample_1km.csv" of the 
"agrodem_sample_input_data" folder in the root directory.