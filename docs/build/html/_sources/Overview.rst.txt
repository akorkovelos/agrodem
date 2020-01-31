Overview
=================================

This documentation is not exhaustive and only serves as a data/process descriptor for the code available on the `project github repo <https://github.com/akorkovelos/agrodem>`_. The aim it to highlight the main methodological steps as well as to provide provide a clearer understanding of the open source code developed to support this exercise. Detailed documentation is available `here <Add link here when ready>`_.

General info
****************

The methodology can be categorized into three main parts as presented in the following figure. The first part includes the collection and preparation of input data, the second includes irrigation modelling processes per se and the third part includes analysis (or post-analysis) and dissemination of the results. 

.. figure::  images/overview_diagram.JPG
   :align:   center

Each part contains several smaller modules. For example the first part includes data collection, downscaling, validation and prepping. Each one of these modules describe a particular activity and is usually characterized by 3 core elements, namely input – process – output. Each process is actualized usually with a piece of code (.ipynb) that requires certain input data to run and generates a particular output. For example, the irrigation model `agrodem <https://github.com/akorkovelos/agrodem/blob/master/agrodem.ipynb>`_ requires two input files (`Sample_Moz_Maize_1km <https://github.com/akorkovelos/agrodem/blob/master/Sample_Moz_Maize_1km.csv>`_ and `Sample_Maize_Crop_Calendar <https://github.com/akorkovelos/agrodem/blob/master/Sample_Maize_Crop_Calendar.xlsx>`_) to run and generates a single output file (`Moz_Maize_1km_Result <https://github.com/akorkovelos/agrodem/blob/master/Sample_results/Moz_Maize_1km_Results.csv>`_) with the results.

Sample input/output files for each process is available on the `project github repo <https://github.com/akorkovelos/agrodem>`_. There one can also access all necessary code. Note that code for the main processes is available in the form of `jupyter notebooks <https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html>`_ (.ipynb) including a clear step-by-step description of how to run as well as reference to sources where needed (e.g. equations, specific values, assumptions etc.). 

This is a geospatial based analysis, therefore some processes require either the installation of spatial libraries in python or the use of a GIS (check `QGIS <https://qgis.org/en/site/>`_) environment. It is recommended that the user uses Python >= 3.5 through `anaconda <https://www.anaconda.com/distribution/>`_ distribution; all required python packages are included in the `requirements <https://github.com/akorkovelos/agrodem/blob/master/requirements.txt>`_ file. Installation of QGIS plugins come with information on installation requirements.


Recommended navigation flow
**************************************
The core of this methodology is the **Irrigation model**. Therefore, it is recommended that a new user starts by opening and navigating through the respective jupyter notebook. It is structured in such way so as to provide a clear step-by-step overview of the modelling process. Sample input/outout files (described above) can be used to test and experiment with the model. 

Once the user develops a better understanding of the model can shift her attention to input data and processes related to generating new or customized input for the model. Relevant code has been developed - and made available – on github. Note however that although code is self-explanatory and replicable to the extent possible, this part is relatively time consuming, resource intensive and might require debugging in both python and QGIS.

A branch of data preparation is related to **“Downscaling”**. That is, creating high resolution input data for the irrigation model based on coarse data sources. This part is optional; the irrigation model can run with coarse data. However, it can be quite useful in cases where data is scares. This covers big part of areas this analysis targets at, for example in Sub-Saharan Africa. 

Note that cross-validation of the downscaling process with actual data might be necessary. Code has been developed; yet is it context specific. That is, it needs to be customized to the user’s individual validation data sources and aspirations.

Finally, once comfortable with the above the user might want to explore **Scenario development**. The code allows for scenario construction that can be flexibly designed depending on purpose covering physical suitability (e.g. extensification), economic feasibility (e.g. intensification, productivity gains), environmental governance (e.g. protected areas) or climate resilience (e.g. heat or flood resilience).