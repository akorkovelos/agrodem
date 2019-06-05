import geopandas as gpd
import rasterio as rio
import fiona
import gdal
import osr
import ogr
import rasterio.mask
import time
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling
from rasterstats import point_query
#from rasterstats import zonal_stats


# STEPS
# 0. Set filepath names - inputs and outputs.
# 1. Read raster, shp data
# 2. Reproject and resample
# 3. Clip data to country boundaries
# 4. Vectorize and extract centroids (our final grid cell 1x1km^2 - at least for now)
# 5. Extract raster values to points

def reproj(inpath, outpath, new_crs, factor):
    dst_crs = new_crs

    with rio.open(inpath) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width*factor, src.height*factor, *src.bounds)
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': dst_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rio.open(outpath, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest)


################### Step 0 ###################

start = time.time()


# Set output filepath
fp = "/Users/kostas/Desktop/agroDemandGIS/outputs/"

# Set initial raster file (Harvest choice 10x10km) path
hcData = "/Users/kostas/Desktop/WBagro/GIS/maiz_h--ssa/maiz_h--SSA.tif"

# Set output raster file name (only projected)
hcData_proj = "maiz_h_proj.tif"

# Set output raster file name (projected + resampled)
hcData_proj_res = "maiz_h_proj_1km.tif"

# Set country boundaries (shp) path
country_fp = '/Users/kostas/Desktop/WBagro/GIS/gadm36_MOZ_shp/gadm36_MOZ_0.shp'

# Set projected country boundaries file name  ? - I get an error otherwise, look below.
country_proj = "MOZ_0_proj.shp"

# Set country, crop output raster file name (1km)
maize_MOZ = "maize_MOZ_1km.tif"

# Set country, crop vectorized data
maize_MOZ_vec = "maize_MOZ_vec.shp"

# Set country, crop vector centroids - points
maize_MOZ_points = "maize_MOZ_points.shp"

# Set country, crop points with maize area (final)
maize_MOZ_grid_cell_1km = "maize_MOZ_grid_cell_1km.shp"

# Set final table (csv) path
maize_MOZ_data = "maize_MOZ_data.csv"

################### Steps 1,2 ###################

#Read initial raster file (HarvestChoice 10x10km^2) - Reproject, resample, and save.
#CRS for Mozambique EPSG:32737 - WGS 84 / UTM zone 37S
reproj(inpath = hcData,
       outpath = fp + hcData_proj_res,
       new_crs = 'EPSG:32737',
       factor = 10)


# Read country boundaries outline - Reproject and save.
mozambique_proj  = gpd.read_file(country_fp).to_crs({'init': 'EPSG:32737'})
mozambique_proj.to_file(fp + country_proj)

################### Step 3 ###################

# Crop raster data to country boundaries - and export.
with fiona.open(fp + country_proj) as shapefile:
    features = [feature["geometry"] for feature in shapefile]


with rio.open(fp + hcData_proj_res) as src:
    out_image, out_transform = rio.mask.mask(src, features,
                                                        crop=True)
    out_meta = src.meta.copy()

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rio.open(fp + maize_MOZ, "w", **out_meta) as dest:
    dest.write(out_image)

################### Step 4 ###################

#Vectorize country area raster, and export polygons (not necessary).

sourceRaster = gdal.Open(fp + maize_MOZ)
band = sourceRaster.GetRasterBand(1)
bandArray = band.ReadAsArray()

srs = osr.SpatialReference()
srs.ImportFromWkt(sourceRaster.GetProjection())

driver = ogr.GetDriverByName("ESRI Shapefile")

# Check if shp already exists
# if os.path.exists(outShapefile+".shp"):
#     driver.DeleteDataSource(outShapefile+".shp")

outDatasource = driver.CreateDataSource(fp + maize_MOZ_vec)
outLayer = outDatasource.CreateLayer("maiz_MOZ_vec", srs=srs)
newField = ogr.FieldDefn('maize_h', ogr.OFTInteger)
outLayer.CreateField(newField)
gdal.Polygonize( band, None, outLayer, 0, [], callback=None )
outDatasource.Destroy()
sourceRaster = None

# Extract polygon centroids and save
polys = gpd.read_file(fp + maize_MOZ_vec)
polys['geometry'] = polys['geometry'].centroid
polys.to_file(fp + maize_MOZ_points)


################### Step 5  ###################
# Reproject original data in order to extract the raster values (Harvest Choice without resampling)
reproj(inpath = hcData,
       outpath = fp + hcData_proj,
       new_crs = 'EPSG:32737',
       factor = 1)

# Reminder
#stats = zonal_stats(fp + maize_MOZ_vec, fp + hcData_proj)
#pts = point_query(fp + maize_MOZ_points, fp + hcData_proj)

data = gpd.read_file(fp + maize_MOZ_points)
data['maize_h_HC'] = point_query(fp + maize_MOZ_points, fp + hcData_proj)
data.to_file(fp + maize_MOZ_grid_cell_1km)

df = data
# How to deal with NaN or -9999 values?
df = data.drop('geometry', axis=1)
df['lon'] = data.geometry.apply(lambda p: p.x)
df['lat'] = data.geometry.apply(lambda p: p.y)

df.to_csv(fp + maize_MOZ_data )


################### Extract GEE image features ###################
# Save and download rasters from @Neeraj GEE extraction code
# Should we automate the downloading from the Drive as well?

gee_path = "/Users/kostas/Desktop/agroDemandGIS/GEE_inputs/"

ndvi ="modis-ndvi.tif"
evi = "modis-evi.tif"

ndvi_proj ="ndvi_proj.tif"
evi_proj = "evi_proj.tif"

reproj(inpath = gee_path+ndvi,
       outpath = gee_path + ndvi_proj,
       new_crs = 'EPSG:32737',
       factor = 1)

reproj(inpath = gee_path+evi,
       outpath = gee_path + evi_proj,
       new_crs = 'EPSG:32737',
       factor = 1)


data['ndvi'] = point_query(fp + maize_MOZ_points, gee_path + ndvi_proj)
data['evi'] = point_query(fp + maize_MOZ_points, gee_path + evi_proj)

data.to_file(fp + "data_GEE.shp")

df = data
df = data.drop('geometry', axis=1)
df['lon'] = data.geometry.apply(lambda p: p.x)
df['lat'] = data.geometry.apply(lambda p: p.y)

df.to_csv(fp + "data_GEE.csv" )

end = time.time()
print("Executed in: {0} mins".format(round((end - start)/60, 2)))