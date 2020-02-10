# agrodem

[![Documentation Status](https://readthedocs.org/projects/agrodem/badge/?version=latest)](https://agrodem.readthedocs.io/en/latest/?badge=latest)

Documentation available [here](https://agrodem.readthedocs.io/en/latest/) (under development)

The **agrodem** model provides an estimate of water and electricity requirements for ground and/or surface water irrigation. It works for one crop at a time. Statial distribution of this crop over the area of interest (AoI) can represent current or projected values. Supporting scripts for downscaling/resampling tabular crop data is also available in this repo. 

## Content

- **Downscaling** directory contains scripts, Qgis plugin and sample files needed to prepare input files to the FLAT model
- **FLAT_model** directory contains scripts supporting the FLAT model
- **Irrigation_model** directory contains scripts, Qgis plugin and sample files needed to prepare input files to the agrodem model
- **agrodem.ipynb** the model
- **pyeto** directory contains contains modules needed to properly run the agrodem.ipynb
- **Sample_results** directory contains indicating results (and html map) of the agrodem model
- **docs** directory contains supporting documentation for running the analysis
- Sample_Moz_Maize_1km.csv 
- Sample_Maize_Crop_Calendar.xlsx

The sample files can be used to estimate maize irrigation needs in Mozambique. **Note!** that input data are not fully representative and results are only indicative.

Visualized, the sample results may look like this:

![SampleResult](SampleResult.png)

## Installation

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

**Note** that ```pyeto``` is also needed and can be installed from https://github.com/woodcrafty/PyETo.git

## Credits

**Conceptualization & Methodological review :** [Alexandros Korkovelos](https://github.com/akorkovelos) & [Konstantinos Pegios](https://github.com/kopegios)<br />
**Code development** [Konstantinos Pegios](https://github.com/kopegios), [Alexandros Korkovelos](https://github.com/akorkovelos) & [Babak Khavari](https://github.com/babakkhavari)<br />
**Review, Updates, Modifications:** [Alexandros Korkovelos](https://github.com/akorkovelos), [Youssef Almulla](https://github.com/JZF07) & [Camilo Ramírez](https://github.com/camiloramirezgo) <br />
**Supervision, Review and Advisory support:** [Mark Westcott](https://www.vivideconomics.com/mark-westcott/), [Neeraj Baruah](https://www.vivideconomics.com/neeraj-baruah/) & [Ines Pozas Franco](https://www.vivideconomics.com/ines-pozas-franco/) <br />
**Funding:** The World Bank (contract number: 7190531), [KTH](https://www.kth.se/en/itm/inst/energiteknik/forskning/desa/welcome-to-the-unit-of-energy-systems-analysis-kth-desa-1.197296)

