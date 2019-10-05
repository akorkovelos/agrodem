# agrodem

[![Documentation Status](https://readthedocs.org/projects/agrodem/badge/?version=latest)](https://agrodem.readthedocs.io/en/latest/?badge=latest)

Documentation available [here](https://agrodem.readthedocs.io/en/latest/)

The **agrodem** model provides an estimate of water and electricity requirements for ground and/or surface water irrigation. It works for one crop at a time. Statial distribution of this crop over the area of interest (AoI) can represent current or projected values. Supporting scripts for downscaling/resampling tabular crop data is also available in this repo. 

## Content

- **Downscaling** directory contains scripts, Qgis plugin and sample files needed to prepare input files to the FLAT model
- **FLAT_model** directory contains scripts supporting the FLAT model
- **Irrigation_model** directory contains scripts, Qgis plugin and sample files needed to prepare input files to the agrodem model

The sample files can be used to estimate maize irrigation needs in Mozambique. **Note!** that input data are not fully representative and results are only indicative.

Visualized in QGIS, sample results look like this:

![SampleResult](SampleResult.png)

## Input requirements
- Sample_Moz_Maize_1km.csv 
- Sample_Maize_Crop_Calendar.xlsx

## Installation

**Install from GitHub**

Download or clone the repository and install the required packages:

```
git clone https://github.com/alekordESA/agrodem.git
cd agrodem
pip install -r requirements.txt
```

**Requirements**

agrodem_pilot requires Python >= 3.5. All required python packages/modules are included in the ```requirements.txt```.
**Note** that ```pyeto``` is also needed and can be installed from https://github.com/woodcrafty/PyETo.git
