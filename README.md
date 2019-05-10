# agrodem_pilot

Documentation: To be updated

Agrodem provides an estimate of water and electricity demand for ground water irrigation.
The current model is designed to run a simple analysis for a selection of crops (maize, cassava) and locations in Mozambique.
Results are solely indicative.

## Input requirements
- Pilot_Input_Crop.csv (per crop)
- Pilot_Input_Crop_Calendar.xlsx (per crop)
- Pilot_Input_Fuel_Prices.xlsx

## Model usage (To be updated)

- Download and install python through anaconda distribution 
- Make sure jupyter notebook is active
- Install requirements as described below
- Open and run notebook in order; Part A - Part B and Part C

## Installation

**Install from GitHub**

Download or clone the repository and install the required packages:

```
git clone https://github.com/alekordESA/agrodem.git
cd agrodem
pip install -r requirements.txt
```

**Requirements**

agrodem_pilot requires Python >= 3.5 with the following packages installed:
- cycler==0.10.0
- kiwisolver==1.1.0
- matplotlib==3.0.3
- numpy==1.16.3
- pandas==0.24.2
- pyparsing==2.4.0
- python-dateutil==2.8.0
- pytz==2019.1
- scipy==1.2.1
- six==1.12.0
- pyeto that can be installed from https://github.com/woodcrafty/PyETo.git
