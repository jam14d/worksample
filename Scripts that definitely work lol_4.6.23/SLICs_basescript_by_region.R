#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-539 TD2_qp_SLICs - Copy//detection results_8.18.22"
path.ano = "C:Analysis_Studies\22-539 TD2_qp_SLICs - Copy\annotation results_8.18.22"
setwd(path.det)

#Tells it to look for all .txt files in the path given above
filelist <- dir(path.det, pattern = ".txt")

#Makes an empty table with number of columns defined by ncol
DataDraft <- data.frame(matrix(ncol = 6))

# Iterate over all files in the detection filelist defined on line 7
i = 1
for(f in 1:length(filelist)){

  # read in detection data
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  
  # change working directory to annotation path on line 3
  # read annotation data into table
  # sum tissue area for current sample
  setwd(path.ano)
  filename <- gsub(" Detections", "", filelist[f])
  Read.Data.ano <- read.table(filename, header=T, sep="\t", fill = TRUE)
  
  # find unique region/section names in detections Parent column
  regionNames <- unique(Read.Data$Parent)
  print("Region names found: ")
  print(regionNames)
  

  # iterate over each region, aggregating data for each individually
  for(regionName in regionNames){
    if(regionName == 'Tumor' | regionName == 'Necrosis' | regionName == 'Other' ){
  
      realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == regionName)
      anoArea <- sum(realAnnotations$Area.µm.2) / 1000000
      setwd(path.det)
    
      # subset negative SLICs and positive SLICs into separate variables
      # and ensure they are child objects of current section/region
      Negative <- subset(Read.Data, Read.Data$Class == "Negative" & Read.Data$Parent == regionName)
      Positive <- subset(Read.Data, Read.Data$Class == "Positive" & Read.Data$Parent == regionName)
      
      # sum the areas of positive and negative SLICs
      # If you're getting NA or 0 in your final data for area metrics, 
      # ensure that an area measurement exists on each SLIC detection in QuPath
      # SLIC area measurements are not assigned by default
      PositiveArea <- sum(Positive$Area.µm.2) / 1000000
      NegativeArea <- sum(Negative$Area.µm.2) / 1000000
    
      DataDraft[i,1] <- gsub(".mrxs.txt", "", filename)
      DataDraft[i,2] <- regionName
      DataDraft[i,3] <- (PositiveArea / anoArea) * 100
      DataDraft[i,4] <- PositiveArea
      DataDraft[i,5] <- NegativeArea
      DataDraft[i,6] <- anoArea

      i = i + 1
    }
  }
}

colnames(DataDraft) <- c("Sample",
                         "Section",
                         "Positive Percent",
                         "Positive Area (mm^2)",
                         "Negative Area (mm^2)", 
                         "Total Tissue Area Analyzed")

#Writes a csv file with the data in the path
write.csv(DataDraft,paste("v2 Data",f,".csv"))
