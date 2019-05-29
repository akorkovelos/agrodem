#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:32:54 2019

@author: NeerajBaruah
"""

import ee
from ee import batch
import time


'''Initialise'''
ee.Initialize()

'''Function to extract GEE image collections'''
def gee_extract(collection, time1, time2, band, desc, output_scale, bounds):     
    
    aoi = ee.Geometry.Rectangle(bounds)
    print("Bounds created. Reading in collection ...")
    dataset = ee.ImageCollection(collection)
    dataset_time = dataset.filterDate(time1, time2)
    bands = dataset_time.select(band)  ## another function for multiple bands - this is for single band only
    composite = bands.median().clip(aoi);   ### Can use different reducer or simpleComposite algorithm
    print("Image composite created ...")
    #print(composite.getInfo())
    
    out = batch.Export.image.toDrive(image=composite, description=desc, scale=output_scale)
    process = batch.Task.start(out)
    print("Initiating download to Google Drive")

'''
##############################
##############################
#######                #######
#######    VARIABLES   #######
#######                #######
##############################
############################## 
'''

'''Input parameters as a list:
       @dataset-collection
       @beginning of compoiste time range
       @end of composite time range
       @band
       @description
       @output spatial resolution
       @area of interest bounds'''

'''Area of interest bounds'''
## Use of bboxfinder - http://bboxfinder.com/#-27.839076,29.882813,-9.795678,41.440430
bounds = [29.882813,-27.839076,41.440430,-9.795678]
      
inputs = [                                                                                      \
          ['MODIS/006/MOD13Q1', '2018-01-01', '2018-12-31', 'NDVI', 'modis-ndvi', 250, bounds], \
          ['MODIS/006/MOD13Q1', '2018-01-01', '2018-12-31', 'EVI', 'modis-evi', 250, bounds],   \
         ]


##############################
##############################
#######                #######
#######       RUN      #######
#######                #######
##############################
##############################
start = time.time()
for i in inputs:
    print("Processing {0} ..." .format(i[4]))
    gee_extract(i[0], i[1], i[2], i[3], i[4], i[5], i[6])

end = time.time()
print("Processed in {0}s" .format(round(end - start,2)))
##############################






##############################
##############################
#######                #######
#######       NOTES    #######
#######                #######
##############################
##############################

## Steps to create virtual env
## Step 1: In terminal - conda create -n ee_py3 -c conda-forge python=3 google-api-python-client pyCrypto spyder jupyter
## Step 2: conda activate ee_py3
## Step 3: pip install earthengine-api
## Step 4: pip install oauth2client
## Step 5: earthengine authenticate
## Step 6: Collect authorisation code from web browser and enter in prompt
## For more info: https://geoscripting-wur.github.io/Earth_Engine/ 

## See https://gis.stackexchange.com/questions/302275/how-to-export-ndvi-image-using-fusion-table-as-featurecollection-boundary-in-gee                                 
## https://github.com/renelikestacos/Google-Earth-Engine-Python-Examples
## https://developers.google.com/earth-engine/datasets/catalog/





