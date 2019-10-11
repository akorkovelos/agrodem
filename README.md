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

Download or clone the repository and install the required packages:

```
git clone https://github.com/alekordESA/agrodem.git
cd agrodem
pip install -r requirements.txt
```

**Requirements**

agrodem_pilot requires Python >= 3.5. All required python packages/modules are included in the ```requirements.txt```.
**Note** that ```pyeto``` is also needed and can be installed from https://github.com/woodcrafty/PyETo.git

## Credits

**Conceptualization & Methodological review :** [Alexandros Korkovelos](https://github.com/akorkovelos) & [Konstantinos Pegios](https://github.com/kopegios)<br />
**Code development** [Konstantinos Pegios](https://github.com/kopegios) & [Alexandros Korkovelos](https://github.com/akorkovelos) <br />
**Review, Updates, Modifications:** [Alexandros Korkovelos](https://github.com/akorkovelos), [Youssef Almulla](https://github.com/JZF07) & [Camilo Ramírez](https://github.com/camiloramirezgo) <br />
**Supervision, Review and Advisory support:** [Mark Westcott](https://www.vivideconomics.com/mark-westcott/), [Neeraj Baruah](https://www.vivideconomics.com/neeraj-baruah/) & [Ines Pozas Franco](https://www.vivideconomics.com/ines-pozas-franco/)
**Funding:** The World Bank (contract number: 7190531), [KTH](https://www.kth.se/en/itm/inst/energiteknik/forskning/desa/welcome-to-the-unit-of-energy-systems-analysis-kth-desa-1.197296)

