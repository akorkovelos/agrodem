# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:44:14 2019

@author: Neeraj Baruah
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


import cropland_scenarios_utilities as cs
import os, time
import pandas as pd
import numpy as np
import gdal


start = time.time()
##############################
##############################
##                          ##          
##          PATHS           ##  
##                          ##
##############################
##############################
DATA_PATH = '~/Electricity_demand/Moz'
TEMP_PATH = '~/Electricity_demand/Moz/temp'
INTERMEDIATE_PATH = '~/Electricity_demand/Moz/intermediate'
OUT_PATH = '~/Electricity_demand/Moz/output'


##############################
##############################
##                          ##          
##          INPUTS          ##  
##                          ##
##############################
##############################
'''1    Input layers for suitability which are categorical (to be reclassified)'''  ## Spatial Layers(s)
input_cat_lyrs = ['moz_landuse_500_clip.tif', 'moz_pas_500_clip.tif'] #, 'moz_flood_rp50_clip_500.tif'] 
'''2    Input layers for suitability which are continuous (to be thresholded)'''    ## Spatial Layers(s) 
input_thr_lyrs = ['moz_pop10_500_clip.tif']
'''3    Input yield layers for major crops'''                                       ## Spatial Layers(s)
input_yield_lyrs = ['cs_rf_low_500_clip_utm.tif'] #########
'''4    Input market areas as points and tiff'''                                    ## Spatial Layer(s)
input_markets = ['moz_markets.shp', 'moz_markets_clip.tif', 'moz_dist2markets_500_clip.tif'] 
'''5    Input production prices'''                                                  ## Spatial Layer(s)
input_prod_prices = ['mz_cost_price_per_ha.tif']                                                     
'''6    Input csv for crop output prices'''                                         ## Data Layer(s)
input_crop_out_prices = ['mz_output_price_per_ha.tif']
'''7    Input administrative bound file'''                                          ## Data Layer(s)
input_bnd = ['moz_bnd.shp']
'''8    Input lookup table for categorical layers'''                                ## Pre-process
input_lut_list = [[(1,1), (2,1), (3,1), (4,0), (5,1), (6,1), (7,1), (8,0), (10,0), (15, 0)], [(0,1), (1, 0), (3,0)]] #, [(0,1), (1,0)]]      ## Forest cover allowed
'''9    Input condition list for continuous layers'''                               ## Pre-process
input_con_list = ['<=::25']
'''10    Input for attainable yield factor as fraction'''                           ## Core param ***
par_ayf = [1] 
'''11   Input for crop prices shock'''                                              ## Core param ***
par_cps = [1] 
'''12   Input WB output price factor'''                                             ## Sensitivity param *
input_wbp = [1]
'''13    Output prices distance decay - Alpha and gamma controls '''                ## Sensitivity param *
o_alpha = [10000]
o_gamma = [0.2]
'''14    Production prices distance decay - Alpha and gamma controls '''            ## Sensitivity param *
p_alpha = [0]
'''15    Future demand for agricultural area (in ha) '''                            ## Core param ***
input_ag_area = [231990] 
'''16    Scenario label'''
sce_nme = ['casBAU']



sce_nme = '_' + sce_nme[0] + '_{0}_{1}_{2}_{3}_{4}_{5}' .format(str(par_ayf[0]).replace('.', '-'), str(par_cps[0]).replace('.', '-'), str(o_alpha[0]).replace('.', '-'), str(o_gamma[0]).replace('.', '-'), str(p_alpha[0]).replace('.', '-'), str(input_ag_area[0]))


##################################
##################################
##                              ##          
##          PROCESSING          ##  
##                              ##
##################################
##################################
'''A    Create binary layers for suitability'''
cs.reclassify_rasters(input_cat_lyrs, lookup_tbl_list=input_lut_list, out_folder = 't')

cs.threshold_rasters(input_thr_lyrs, condition_list=input_con_list, out_folder = 't')


'''B    Create suitability layer'''
suitability_file = cs.sf('suitability{0}.tif' .format(sce_nme), 'o')
cs.multiply_binary_rasters(cs.iterateRasters(TEMP_PATH, '*_sbin.tif'), suitability_file) 


'''C    Create yield layer '''
yield_file = cs.sf('ma_yield{0}.tif' .format(sce_nme), 'i')
cs.weighted_sum(input_yield_lyrs, par_ayf, yield_file)


'''D    Create distance from markets'''
#mar_dist = cs.sf('dist_2_markets{0}.tif' .format(sce_nme), 'i')
#cs.distRasters(input_markets[1], mar_dist)
mar_dist = cs.sf(input_markets[2], 'd')


'''D    Get farmgate output prices and production costs for revenue'''
output_prices = cs.sf('output_prices{0}.tif' .format(sce_nme), 'o')
cs.o_distance_decay(input_crop_out_prices[0], mar_dist, o_alpha[0], o_gamma[0], par_cps[0], output_prices)

cost_prices = cs.sf('cost_prices{0}.tif' .format(sce_nme), 'o')
cs.p_distance_decay(input_prod_prices[0], mar_dist, p_alpha[0], input_wbp[0], cost_prices)



'''E    Get gross revenue and profitability'''
gross_revenue = cs.sf('gross_revenue{0}.tif' .format(sce_nme), 'o')
cs.array_calc(yield_file, output_prices, gross_revenue, calc = '*')

revenue = cs.sf('revenue{0}.tif' .format(sce_nme), 'o')
cs.array_calc(gross_revenue, cost_prices, revenue, calc = '-')
cs.array_calc(suitability_file, revenue, revenue, calc = '*')    ## clip it by suitability


'''F    Final raster clip'''
final_layer = cs.sf('profitability{0}.tif' .format(sce_nme), 'o')
cs.raster_clip(revenue, input_bnd[0], final_layer)


'''G    Get binary cropland values (threshold)'''
cs.threshold_rasters([revenue], condition_list=['>::0'], out_folder = 't')
rev_nme = revenue.split('.')[0] + '_sbin.tif'
arr = cs.getRaster(rev_nme)
u,v = np.unique(arr, return_counts=True)
print(u,v)




threshold = cs.get_threshold(revenue, pixels = cs.area_to_pixels(demand = input_ag_area[0], unit = 'ha', pixel_size = 500))

cs.threshold_rasters([revenue], condition_list = ['>=::{0}' .format(str(threshold))], out_folder = 'o')



end = time.time()
print("Processed in {0}s" .format(round(end - start,2)))

