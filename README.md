# agrodem

[![Documentation Status](https://readthedocs.org/projects/agrodem/badge/?version=latest)](https://agrodem.readthedocs.io/en/latest/?badge=latest)

Documentation available [here](https://agrodem.readthedocs.io/en/latest/).

The **agrodem** model provides an estimate of water and electricity requirements for ground and/or surface water irrigation. It works for one crop at a time. Statial distribution of this crop over the area of interest (AoI) can represent current or projected values. This repository provides code, material (to the extent possible) and instructions for replicating and/or customizing the model as needed.

## Content

- **agrodem.ipynb** contains the core code of the irrigation model
- **agrodem_sample_input_data** directory contains sample input data for testing; data represent 1000 maize locations in Mozambique
	- Pilot_Moz_Maize_Sample_1km.csv
	- Pilot_Input_Crop_Calendar_Maize.xlsx
- **agrodem_sample_output_data** directory contains indicative results of the agrodem model
	- Sample_Moz_Maize_2017_1km_Results.csv
	- map_Moz_Maize_sample_2017.html
- **pyeto** directory contains modules needed to properly run agrodem.ipynb
- **docs** directory contains supporting project documentation
- **agrodem_preprocessing** directory contains scripts, Qgis plugins and sample files needed to prepare input files to the agrodem model
	- Agrodem_Preping
	- Downscaling (FLAT model)
	- Future scenarios
- **agrodem_postprocessing** directory contains scripts and sample files related to post analysis 
	- Post-harvesting
	- Crossvalidation
- **agrodem_environment.yml** environment info for setting up package requirements related only to the agrodem.ipynb
-**full_project_environment.yml** environment info for setting up package requirements for all supporting processes in this repository

**Note!** that sample input/output data are not fully representative but only indicative for Mozambique.

## Setting up the environment & running the model

**Install from GitHub**

Download repository directly or clone it to you designated local directory using:

```
git clone https://github.com/alekordESA/agrodem.git
```

**Requirements**

The agrodem module (as well as all supporting scripts in this repo) have been developed in Python 3. We recommend installing [Anaconda's free distribution](https://www.anaconda.com/distribution/) as suited for your operating system. 

Once installed, open anaconda prompt and move to your local "agrodem" directory using:

```
> cd ..\agrodem
```

In order to be able to run the agrodem model (agrodem.ipynb) you should install all necessary packages. "agrodem_environment.ylm" contains all of these and can be easily set up by creating a new virtual environment using:

```
conda env create --name agrodem_run --file agrodem_environment.ylm
```

This might take a while.. When complete, activate the virtual environment using:

```
conda activate agrodem_run 
```

With the environment activated, you can now move to the agrodem directory and start a "jupyter notebook" session by simply typing:

```
..\agrodem> jupyter notebook 
```

**Note 1** Use ```full_project_environment.yml``` under the same instructions to set up a supporting environment for all processes described in this repo.

**Note 2** that ```pyeto``` is also needed and can be installed from https://github.com/woodcrafty/PyETo.git


## Credits

**Conceptualization & Methodological review :** [Alexandros Korkovelos](https://github.com/akorkovelos) & [Konstantinos Pegios](https://github.com/kopegios)<br />
**Code development** [Konstantinos Pegios](https://github.com/kopegios), [Alexandros Korkovelos](https://github.com/akorkovelos) & [Babak Khavari](https://github.com/babakkhavari)<br />
**Review, Updates, Modifications:** [Alexandros Korkovelos](https://github.com/akorkovelos), [Youssef Almulla](https://github.com/JZF07) & [Camilo Ramírez](https://github.com/camiloramirezgo) <br />
**Supervision, Review and Advisory support:** [Mark Westcott](https://www.vivideconomics.com/mark-westcott/), [Neeraj Baruah](https://www.vivideconomics.com/neeraj-baruah/) & [Ines Pozas Franco](https://www.vivideconomics.com/ines-pozas-franco/) <br />
**Funding:** The World Bank (contract number: 7190531), [KTH](https://www.kth.se/en/itm/inst/energiteknik/forskning/desa/welcome-to-the-unit-of-energy-systems-analysis-kth-desa-1.197296)

