## Data check for FLAT 
## Coded by Jingyu Song
## 02082016
## Updated 05212016, added dataset checks for projection

#########################################################
## Command line arguments extracted to R
#########################################################

args <- commandArgs("TRUE")
#args <- list('MOZ_points_260619_FINAL_NONZERO.csv', 1, 1, 16)

Inputs <- args[1] # refers to the selected dataset for estimation, it can be the default maize, default multi-crop, or user uploaded dataset.
                  # default maize dataset is named "defaultmaizedataset.csv" and default multi-crop dataset is named "defaultmulticropdataset.csv"

#Projectioninputs <- args[2]# refers to the selected dataset for projection.

GridSize <- as.numeric(args[2]) # Gridcell size, which is set by the "Choose Grid Size" drop down box.e.g.5 by 5 pixel size means GridSize = 5  
M <- as.numeric(args[3]) # number of dependent variables
N <- as.numeric(args[4]) # number of independent variables

data <- read.csv(as.character(Inputs),header = TRUE)
#prodata <- read.csv(Projectioninputs,header = TRUE)

#data <- read.csv("points_test.csv",header = TRUE)
#prodata <- read.csv("data_tidy_final_proj.csv",header = TRUE)
####################################################################
#############                                     ##################
#############        Perform Data Checks          ##################
#############                                     ##################
####################################################################

#######################################################
## Check for pixel identifier duplicates 
#######################################################
if (anyDuplicated(data[1])) {
  print("Error: pixel identifiers are not unique for the estimation dataset")
} else {
  print("Unique pixel identifiers loaded successfully for the estimation dataset")
}


# if (anyDuplicated(prodata[1])) {
#   print("Error: pixel identifiers are not unique for the projection dataset")
# } else {
#   print("Unique pixel identifiers loaded successfully for the projection dataset")
# }



#######################################################
## Check for missing data 
#######################################################
if (anyNA(data)) {
  print("Error: the data for estimation contains missing values")
} else {
  print("No missing values in the dataset for estimation")
}


# if (anyNA(prodata)) {
#   print("Error: the data for projection contains missing values")
# } else {
#   print("No missing values in the dataset for projection")
# }


#######################################################
## Check degree of freedom
#######################################################
if (nrow(unique(data[2])) < (M*N)) {
  print("Warning: more independent variables than observations for the estimation dataset")
} else {
  print("Degrees of freedom checked for estimation")
}

#######################################################
## Check for space in state names 
#######################################################
nospace <- grepl(" ", data[,2])
if (table(nospace)["FALSE"] == nrow(data[2])) {
  print("State names meet format requirements for estimation")
} else {
  print("Error: the state names contain spaces in the estimation dataset; please delete the spaces")
}


# nospace <- grepl(" ", prodata[,2])
# if (table(nospace)["FALSE"] == nrow(prodata[2])) {
#   print("State names meet format requirements for projection")
# } else {
#   print("Error: the state names contain spaces in the projection dataset; please delete the spaces")
# }


#######################################################
## Check for full rank
#######################################################
#install.packages("matrixcalc")
library(matrixcalc)
X <- as.matrix(data[,(6+M):(5+M+N)])
XX <- t(X) %*% X
if (is.positive.definite(XX)) {
  print("Estimation dataset full rank")
} else {
  print("Error: dataset for estimation rank deficient")
}


#######################################################
## Check uniformity for datasets
#######################################################
# if (length(data)==length(prodata)) {
#   print("Estimation and projection datasets have the same number of columns")
# } else {
#   print("Error: estimation and projection datasets have different number of columns")
# }



####################################################################
#############                                     ##################
#############  Generate Data Files for Estimation ##################
#############                                     ##################
####################################################################

#######################################################
## Extract pixels 
#######################################################
write.table(data[1],"pixels.csv",row.names=FALSE,col.names=FALSE)

#######################################################
## Extract states 
#######################################################
write.table(unique(data[2]),"states.csv",row.names=FALSE,col.names=FALSE)


#######################################################
## Extract state level crop area info
#######################################################
write.csv(cbind(unique(data[,c(2,6:(5+M))])) ,"statelevelcroparea.csv",row.names=FALSE)
#######################################################
## Extract depdendent variable (crop) names 
#######################################################
write.table(colnames(data[c(6:(5+M))]),"cropnames.csv",row.names=FALSE,col.names=FALSE)

#######################################################
## Extract independent variables 
#######################################################
write.csv(cbind(data[,c(1:2,(6+M):(5+M+N))]),"data.csv",row.names=FALSE)

#######################################################
## Extract pixel area and coordinates info 
#######################################################
pixelarea <- (2*acos(0)*6371^2*(GridSize/60/180)*(cos((90-data[4])/360*4*acos(0))-cos(((90-data[4])+GridSize/60)/360*4*acos(0))))*100
colnames(pixelarea) <- 'pixelarea'
write.csv(cbind(data[,c(1:4)],pixelarea),"pixelarea.csv",row.names=FALSE)

#######################################################
## Generate state level total area info
## Check if total crop area provided is smaller than total state area
#######################################################
X <- data.frame(pixelarea,data[,c(1:2,5:(5+M))])
#X<-X[order(X$alloc_key),]
#X <- X[X$maize/X$statearea>0.005, ] 
name <- levels(X$NAME)
state <- list()
area <- list()
totalcrop <- list()
crop <- list()

#counter=0
for (i in 1:length(name)){
  #print ("i")
  #print(i)
  #print(X[which(X$NAME == name[i]),])
  state[[i]] <- X[which(X$NAME == name[i]),]
  #print("First")
  #print(state[[i]][1,4])
  area[[i]] <- state[[i]][1,4]
  #print("second")
  #print(state[[i]][1,5:(4+M)])
  totalcrop[[i]] <- sum(state[[i]][1,5:(4+M)])
  crop[[i]] <- state[[i]][1,5:(4+M)]
  #counter=+1
}

totalcroparea <- unlist(totalcrop)
statearea <- unlist(area)
croparea <- matrix(unlist(crop),ncol=M,nrow=length(name),byrow=TRUE)
#croparea <- unlist(crop)

if (all((totalcroparea - statearea) < 0)) {
  print("Total area in included crops is smaller than total state area for the estimation dataset")
} else {
  print("Error: total crop area provided by user is greater than total state area for the estimation dataset")
}

if (all(croparea/statearea > 0.005)) {
  print("Each crop takes more than 0.5% of total state area")
} else {
  print("Warning: uploaded dataset contains states with crop area less than 0.5% of total state area, may consider dropping such states")
}

statearea <- as.numeric(unlist(area))
table <- data.frame(name,statearea)
names(table) <- c("NAME","statearea")
write.table(table,"statelevelareainfo.csv",sep=",",row.names=FALSE,col.names=FALSE)

#(croparea/statearea )
#######################################################
## Extract independent variable names 
#######################################################
write.table(colnames(data[(6+M):(5+M+N)]),"names.csv",row.names=FALSE,col.names=FALSE)

#######################################################
## Create set "index" for use in GAMS script  
#######################################################
number <- seq(1,length(data[,(6+M):(5+M+N)])*M,by = 1)
index <- paste("x",number,sep="")
write.table(index,"variables.csv",row.names=FALSE,col.names=FALSE)




####################################################################
#############                                     ##################
#############  Generate Data Files for Projection ##################
#############                                     ##################
####################################################################

#######################################################
## Extract pixels 
#######################################################
# write.table(prodata[1],"projectionpixels.csv",row.names=FALSE,col.names=FALSE)
# 
# #######################################################
# ## Extract states 
# #######################################################
# write.table(unique(prodata[2]),"projectionstates.csv",row.names=FALSE,col.names=FALSE)
# 
# 
# #######################################################
# ## Extract state level crop area info
# #######################################################
# write.csv(cbind(unique(prodata[,c(2,6:(5+M))])) ,"projectionstatelevelcroparea.csv",row.names=FALSE)
# 
# #######################################################
# ## Extract independent variables 
# #######################################################
# write.csv(cbind(prodata[,c(1:2,(6+M):(5+M+N))]),"projectiondata.csv",row.names=FALSE)
# 
# #######################################################
# ## Extract pixel area and coordinates info 
# #######################################################
# propixelarea <- (2*acos(0)*6371^2*(GridSize/60/180)*(cos((90-prodata[4])/360*4*acos(0))-cos(((90-prodata[4])+GridSize/60)/360*4*acos(0))))*100
# 
# projectionpixelarea <- cbind(prodata[,c(1:4)],propixelarea)
# colnames(projectionpixelarea) <- c("alloc_key","NAME","projectionlon","projectionlat","projectionpixelarea")
# 
# write.csv(projectionpixelarea,"projectionpixelarea.csv",row.names=FALSE)
# 
# #######################################################
# ## Generate state level total area info
# ## Check if total crop area provided is smaller than total state area
# #######################################################
# proX <- data.frame(propixelarea,prodata[,c(1:2,5:(5+M))])
# proname <- factor(proX$NAME)
# prostate <- list()
# proarea <- list()
# prototalcrop <- list()
# procrop <- list()
# 
# for (i in 1:length(proname)){
#   prostate[[i]] <- proX[which(proX$NAME == proname[i]),]
#   proarea[[i]] <- prostate[[i]][1,4]
#   prototalcrop[[i]] <- sum(prostate[[i]][1,5:(4+M)])
#   procrop[[i]] <- prostate[[i]][1,5:(4+M)]
# }
# 
# prototalcroparea <- unlist(prototalcrop)
# prostatearea <- unlist(proarea)
# procroparea <- matrix(unlist(procrop),ncol=M,nrow=length(proname),byrow=TRUE)
# 
# if (all((prototalcroparea - prostatearea) < 0)) {
#   print("Total area in included crops is smaller than total state area for the projection dataset")
# } else {
#   print("Error: total crop area provided by user is greater than total state area for the projection dataset")
# }
# 
# 
# prostatearea <- as.numeric(unlist(proarea))
# protable <- data.frame(proname,prostatearea)
# names(protable) <- c("NAME","statearea")
# write.table(protable,"projectionstatelevelareainfo.csv",sep=",",row.names=FALSE,col.names=FALSE)
# 
# 
# #######################################################
# ## Check de-/independent variable names 
# #######################################################
# prodependentvar <- colnames(prodata[c(6:(5+M))])
# dependentvar <- colnames(data[c(6:(5+M))])
# count=0
# for (i in 1:max(length(prodependentvar),length(dependentvar))){
# if (prodependentvar[i] == dependentvar[i]) {
#   count = count+1}
# }
# 
# if (count == max(length(prodependentvar),length(dependentvar))){
#   print("Dependent variables in estimation and projection datasets are identical")
# } else {
#   print("Error: dependent variables in estimation and projection datasets are different")
# }
# 
# proindependentvar <- colnames(prodata[(6+M):(5+M+N)])
# independentvar <- colnames(data[(6+M):(5+M+N)])
# count=0
# for (i in 1:max(length(proindependentvar),length(independentvar))){
# if (proindependentvar[i] == independentvar[i]) {
#   count = count+1}
# }
# 
# if (count == max(length(proindependentvar),length(independentvar))){
#   print("Independent variables in estimation and projection datasets are identical")
# } else {
#   print("Error: independent variables in estimation and projection datasets are different")
# }




