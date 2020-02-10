#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 11:21:08 2019

@author: NeerajBaruah
"""

###############################################################################
# 
#
# Project:  World Bank AgriDemand Cropland scenarios
# Purpose:  Functions which aid in cropland scenario analysis (Chamberlin 2014)
#           
# Author:   Neeraj Garg Baruah, n.g.baruah@vivideconomics.com
#
###############################################################################
# Copyright (c) 2019, Neeraj Garg Baruah <n.g.baruah@vivideconomics.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################



import glob
from osgeo import gdal, ogr, osr
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import numpy as np
import rasterio
from rasterio.mask import mask
import fiona
import os



DATA_PATH = '~/Electricity_demand/Moz'
TEMP_PATH = '~/Electricity_demand/Moz/temp'
INTERMEDIATE_PATH = '~/Electricity_demand/Moz/intermediate'
OUT_PATH = '~/Electricity_demand/Moz/output'



#################
'''
SET WORK FOLDER
'''
#################
def sf(outname, path='i'):
    ### Default as intermediate path
    ### sf - set folder
    
    if path == 'i':
        return os.path.join(INTERMEDIATE_PATH, outname)
    elif path == 't':
        return os.path.join(TEMP_PATH, outname)
    elif path == 'o':
        return os.path.join(OUT_PATH, outname)
    elif path == 'd':
        return os.path.join(DATA_PATH, outname)
    else:
        print("Please enter folder path as one of below: i - intermediate, t - temp, o - output, d - data, r - rasterpath")


'''
    Iterate rasters in a folder and get a list
'''
def iterateRasters(folder_nme, wildcard):
    pathlist = glob.glob(os.path.join(folder_nme, wildcard))
    
    paths = []
    for path in pathlist:         
         path_in_str = str(path)
         paths.append(path_in_str)
    return paths
        


'''
    Get raster as band or array output from raster file name
'''
def getRaster(rst_nme, band=1, asArray=1):
    
    if isinstance(rst_nme, np.ndarray):
        arr = rst_nme
    else:        
        rst = gdal.Open(rst_nme)
        band_data = rst.GetRasterBand(band)
        arr = BandReadAsArray(band_data)     
        
    if asArray == 1:
        
        return arr
    else:
        return band
    

'''
    Output array as raster
'''
def arr2rst(ref_rst, arr, output_file, file_type=gdal.GDT_Byte):
    
    ref = gdal.Open(ref_rst, GA_ReadOnly)
    band = ref.GetRasterBand(1)
    proj = ref.GetProjection()
    geotransform = ref.GetGeoTransform()
    xsize = band.XSize
    ysize = band.YSize
    
    gtiff = gdal.GetDriverByName('GTiff') 
    out = gtiff.Create(output_file, xsize, ysize, 1, file_type)
    out.SetProjection(proj)
    out.SetGeoTransform(geotransform)
    
    
    out.GetRasterBand(1).WriteArray(arr) 
    out.FlushCache()
    out = None
 


'''
    Convert arrays to a multi band raster
''' 
def CreateGeoTiff(output_file, Array, ref_rst):
#    Array[np.isnan(Array)] = NDV
    ref = gdal.Open(ref_rst, GA_ReadOnly)
    band = ref.GetRasterBand(1)
    proj = ref.GetProjection()
    geotransform = ref.GetGeoTransform()
    xsize = band.XSize
    ysize = band.YSize
    num_bands = Array.shape[2]
    
    
    gtiff = gdal.GetDriverByName('GTiff')
    DataSet = gtiff.Create(output_file, xsize, ysize, num_bands, gdal.GDT_Byte)
    DataSet.SetGeoTransform(geotransform)
    DataSet.SetProjection(proj)
    
    for i in range(1, num_bands):
            arr = Array[:,:,i]
            
            DataSet.GetRasterBand(i).WriteArray(arr)
        
#        DataSet.GetRasterBand(i).SetNoDataValue(NDV)
        
    DataSet.FlushCache()
    


'''
    RESAMPLE
'''
###############################################################################
# 
#
# TO DO : Resample raster grid using multiple algos - nearest neighbour, average, median, majority.
# 
# Source: https://gis.stackexchange.com/questions/234022/resampling-a-raster-from-python-without-using-gdalwarp          
# 
#
###############################################################################

def resample():
    from osgeo import gdal, gdalconst
    
    inputfile = r"C:\Users\Development\Downloads\mini_mozambique.tif"
    inputf = gdal.Open(inputfile)
    inputProj = inputf.GetProjection()
#    inputTrans = inputf.GetGeoTransform()
    
    referencefile = r"C:\Users\Development\Downloads\MODIS_landcover\MCD12Q1.A2010001.h21v10.006.2018146000538.hdf"
    reference1 = gdal.Open(referencefile)
    reference = gdal.Open(reference1.GetSubDatasets()[0][0])
    referenceProj = reference.GetProjection()
    referenceTrans = reference.GetGeoTransform()
#    bandreference = reference.GetRasterBand(1)    
    x = reference.RasterXSize 
    y = reference.RasterYSize
    print(type(x),type(y))
    print(referenceProj)
    print(referenceTrans)
    
    
    outputfile = "1km_downscaled.tif"
    driver= gdal.GetDriverByName('GTiff')
    print(type(outputfile),type(x),type(y))
    output = driver.Create(outputfile,x,y,1,gdal.GDT_Float32)
    output.SetGeoTransform(referenceTrans)
    output.SetProjection(referenceProj)
    
    gdal.ReprojectImage(input,output,inputProj,referenceProj,gdalconst.GRA_Bilinear)

    del output


'''
    RASTERISE
'''
###############################################################################
# 
#
# TO DO: Convert shapefile of points and polygons into raster (burn 1, or by attribute)
# 
# Souce: https://gis.stackexchange.com/questions/212795/rasterizing-shapefiles-with-gdal-and-python         

def rasterise(Shapefile_path,Output_filename):


    
    
    # 1) opening the shapefile    
    
    source_ds = ogr.Open(Shapefile_path)
    source_layer = source_ds.GetLayer()
    
    
    # 2) Creating the destination raster data source
    
    pixelWidth = pixelHeight = 0.1 # depending how fine you want your raster ##COMMENT 1
    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    cols = int((x_max - x_min) / pixelHeight)
    rows = int((y_max - y_min) / pixelWidth)
    
    target_ds = gdal.GetDriverByName('GTiff').Create(Output_filename, cols, rows, 1, 
    gdal.GDT_Float32) ##COMMENT 2
    
    target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_max, 0, -pixelHeight) )##COMMENT 3
    
    # 5) Adding a spatial reference ##COMMENT 4
    target_dsSRS = osr.SpatialReference()
    target_dsSRS.ImportFromEPSG(32736)
    target_ds.SetProjection(target_dsSRS.ExportToWkt())
    
    band = target_ds.GetRasterBand(1) 
    band.SetNoDataValue(0) ##COMMENT 5
    
    gdal.RasterizeLayer(target_ds, [1], source_layer,burn_values=[1], options=["ALL_TOUCHED=TRUE"]) ##COMMENT 6
    
    target_ds = None ##COMMENT 7
    


'''
    Majority filter
'''
def majority_filter(raster, mask_rst, exclude):
    arr = getRaster(raster, band=1, asArray=1)
    arr = arr.astype(np.float16)
    marr = getRaster(mask_rst, band=1, asArray=1)
    u,v = np.unique(arr, return_counts=True)
    print(u)
    for e in exclude:
        arr[arr == e] = np.nan
    u,v = np.unique(arr, return_counts=True)
    print(u)



'''
    Calculate distance to features marked with 1 in a raster
'''
def distRasters(rst, outnme):
    ref = gdal.Open(rst, GA_ReadOnly)
    band = ref.GetRasterBand(1)
    proj = ref.GetProjection()
    geotransform = ref.GetGeoTransform()
    xsize = band.XSize
    ysize = band.YSize
    
    gtiff = gdal.GetDriverByName('GTiff')
    DataSet = gtiff.Create(outnme, xsize, ysize, 1, gdal.GDT_UInt16)
    DataSet.SetGeoTransform(geotransform)
    DataSet.SetProjection(proj)
    
    options = []
    
    gdal.ComputeProximity(band, DataSet.GetRasterBand(1), options, callback = None)



'''
    Clip raster using a mask
'''
def clipRaster(raster, mask, outnme, filetype=GDT_Float32):
    arr = getRaster(raster, band=1, asArray=1)
    mask_arr = getRaster(mask, band=1, asArray=1)
    
    arr = arr*mask_arr
    arr2rst(raster, arr, outnme,  file_type=filetype)
    


'''
    Reclassify a raster numpy array using a look-up table in the form of a tuple-list
'''
def reclassify_rasters(raster_list, lookup_tbl_list, out_folder = 'i'):
    '''For only categorical values'''
    #lookup_tbl = [(old_value_1, new_value_1), (old_value_2, new_value_2), ...] is the format
    ### May need to clip
    
    counter = 0
    for r in raster_list:
        print(r)
        
        rst_nme = r.split('.')[0] + '_sbin.tif'  ## to change
        rst_arr = getRaster(r, band=1, asArray=1)
        rst_arr = rst_arr.astype(np.uint16)
        
        idx, val = np.asarray(lookup_tbl_list[counter]).T
        lookup_array = np.zeros(max(idx) + 1)

        lookup_array[idx] = val

        new_array = lookup_array[rst_arr]

        
        arr2rst(r, new_array, sf(rst_nme, out_folder), file_type=gdal.GDT_UInt16)
        counter = counter + 1
        

'''
    Threshold rasters based on conditions
'''
def threshold_rasters(raster_list, condition_list, out_folder = 'i'):
    '''
    Condition list of the form - ['>::12', '<=::3']
    '''
    ## May need to clip
    
    counter = 0
    for r in raster_list:
        rst_nme = r.split('.')[0] + '_sbin.tif'  ## to change
        rst_arr = getRaster(r, band=1, asArray=1)
        
        cond = condition_list[counter].split('::')[0]
        thresh = float(condition_list[counter].split('::')[1])
        
        if cond == '<':
            rst = np.where(rst_arr < thresh, 1, 0)
        elif cond == '>':
            rst = np.where(rst_arr > thresh, 1, 0)
        elif cond == '<=':
            rst = np.where(rst_arr <= thresh, 1, 0)
        elif cond == '>=':
            rst = np.where(rst_arr >= thresh, 1, 0)
        elif cond == '==':
            rst = np.where(rst_arr == thresh, 1, 0)
        elif cond == '!=':
            rst = np.where(rst_arr != thresh, 1, 0)
        else:
            print("Only >, <, >=, <=, == and != are allowed!")
        
        arr2rst(r, rst, sf(rst_nme, out_folder), file_type=gdal.GDT_Byte)
        counter = counter + 1
        
            

'''
    Multiply binary rasters
'''
def multiply_binary_rasters(rasters, outnme):
    rst = getRaster(rasters[0])
    
    for r in rasters[1:]:
        ar = getRaster(r)
        rst = rst*ar

    arr2rst(rasters[0], rst, outnme, file_type=gdal.GDT_Byte)
           


'''
    Create weighted sum of rasters
'''
def weighted_sum(raster_list, weights_list, outnme):
    rst = getRaster(raster_list[0]) * weights_list[0]
    
    if len(raster_list) > 1:
        counter = 1
        for r in raster_list[1:]:
            ar = getRaster(r)
            rst = rst + (ar * weights_list[counter])
            counter = counter + 1
    
    arr2rst(raster_list[0], rst, outnme, file_type=gdal.GDT_Float32)
    


'''
    Distance decay equation (negative exp)
'''
def o_distance_decay(prices_file, dist_file, alpha, gamma, shock_factor, output):
    
    distance_raster = getRaster(dist_file, band=1, asArray=1)
    output_price = getRaster(prices_file, band=1, asArray=1)
    output_price = output_price * shock_factor
    
    base_decay = 1.0 - (np.exp((-alpha/distance_raster))*gamma)
    arr2rst(prices_file, base_decay, 'basedecay_test.tif', file_type=gdal.GDT_Float32)
    o_decay = output_price * base_decay
    arr2rst(prices_file, o_decay, output, file_type=gdal.GDT_Float32)
 

'''
    Distance decay equation (positive exp)
'''
def p_distance_decay(costs_file, dist_file, alpha, suppress, output):
    
    distance_raster = getRaster(dist_file)
    cost_price = getRaster(costs_file)
    cost_price = cost_price * suppress
    
    base_decay = np.exp(alpha * distance_raster)
    p_decay = cost_price * base_decay
    arr2rst(costs_file, p_decay, output, file_type=gdal.GDT_Float32)

    
'''
    Array calculator
'''
def array_calc(a,b, output, calc = '-', filetype = gdal.GDT_Float32):
    
    a_ar = getRaster(a)
    b_ar = getRaster(b)   
    
    if calc == '*':
        f = a_ar * b_ar
    elif calc == '+':
        f = a_ar + b_ar
    elif calc == '-':
        f = a_ar - b_ar
    elif calc == '/':
        f = a_ar/b_ar
    else:
        print("Please enter calc as one of: *, +, -, /")
      
    arr2rst(a, f, output, file_type=filetype)
    
 
def raster_clip(Input_raster_path,vector_clip_path, outnme):
    """
     This function clips a raster file with a provided polygon and writes the 
     result to a geotiff file
    
    Inputs
    Input_raster_path - Full file path to raster file 
    vector_clip_path - Full file path to shapefile to be used in clipping the raster file
    """
    with fiona.open(vector_clip_path) as shapefile:
        geoms = [feature["geometry"] for feature in shapefile]
    with rasterio.open(Input_raster_path) as src:
        out_image, out_transform = mask(src, geoms, crop=True)
    out_meta = src.meta.copy()
    
    # save the resulting raster  
    out_meta.update({"driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
    "transform": out_transform})
    
    with rasterio.open(outnme, "w", **out_meta) as dest:
        dest.write(out_image)   
    


'''
    Get pixel size
'''
def getPixelValue(rst):
    ds = gdal.Open(rst)
    gt = ds.GetGeoTransform()
    pixelSize = round(gt[1],0)
 
    return pixelSize



'''
    Convert area demand to pixels
'''
def area_to_pixels(demand, unit = 'km2', pixel_size = 30):
#    demand = demand[0]
    pixel_area = pixel_size * pixel_size
    if unit == 'km2':
        pixels = int(round((demand*1000000.0)/(pixel_area),0))
    elif unit == 'm2':
        pixels = int(round((demand)/(pixel_area),0))
    elif unit == 'ha':
        pixels = int(round((demand*10000.0)/(pixel_area),0))   
    else:
        print("Demand should be in m2, km2 or ha")
        
    return pixels



'''
    Convert potential raster to urban forecasts using number of pixels to convert
'''
def get_threshold(potential_raster, pixels):
  
    urb_pot = getRaster(potential_raster)    
    urb_pot = urb_pot[urb_pot > 0]
    
    u,v = np.unique(urb_pot, return_counts=True)
    total_avail_pixels = sum(v)
    thresh = sorted(urb_pot, reverse=True)[:pixels][-1] 
    
    return(thresh)
    

    