## Jingyu Song
## 04/05/2016
## make a tiff file for the results

################################
## get command line arguments ## 
################################

#args <- commandArgs(TRUE)

#crop <- "maize" # selected crop to map.
#input <- "finalresults.dat" #input finalresults.dat

##############################
## Load the dat result file ##
##############################

#data <- read.delim(input, header = TRUE,sep = "") 
# sep = "" denotes white space, i.e. there is one or more spaces being the delimiter
data <- read.table("finalresults.dat", header=TRUE)
data$MaizeArea <- data$Fraction*81.8963461156
head(data)
write.csv(data, file = "finalresults_020719.csv")

########################################
## get fractions for the crop to map  ##
########################################

coord <- as.matrix(data[,c("lon","lat")])

for (i in (1:ncol(data)))
{ if (crop == data[2,i])
  { coord <- cbind(coord,data[,(i+1)])
  }
}


##############################
## convert to tiff file     ##
##############################
require(raster)
e <- extent(coord[,c(1,2)])
# Create a raster object r 
r <- raster(e, ncol=ceiling((max(coord[,1])-min(coord[,1]))/0.083333), nrow=ceiling((max(coord[,2])-min(coord[,2]))/0.083333))
x <- rasterize(coord[,c(1,2)], r, coord[,3], fun=mean)
x[is.na(x[])] <- -1
#tifffn <- basename(tempfile('out', fileext='.tif'))
tifffn <- basename(paste('out-', crop, '.tif', sep=''))
tiffpath <- paste('local://', tifffn, sep='')
x.sp <- as(x,"SpatialPixelsDataFrame")
proj4string(x.sp) <- CRS('+proj=longlat +datum=WGS84 +no_defs')
require(rgdal)
fig <- writeGDAL(x.sp,tifffn,drivername="GTiff")



