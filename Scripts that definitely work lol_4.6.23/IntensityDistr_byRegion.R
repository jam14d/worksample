##FINAL SCRIPT - 

#Change path here, this is where your data is
path.det = "D://23-159 Grace_spc_qp//detections_binnedspc"
path.ano = "D://23-159 Grace_spc_qp//annotations_binnedspc"

setwd(path.ano)
filelistano <- sort(dir(path.ano,pattern = ".txt"))

setwd(path.det)
filelist <- sort(dir(path.det,pattern = ".txt"))

#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 24))

#This is a counter, set it equal to 1 outside of the for loop, within the for loop we increase it (k = k + 1) 
#through each pass through the loop to have a counter for each row of data, so first .txt file goes in k = 1 row, second is k = k + 1 row etc..

k = 1
#For loop, for every file ending in .txt in that path, we will run through this loop of calculations once.  
#perhaps change this to a while loop --> while filelist[1] == filelistano[1]  (kills 2 birds with 1 stone)
for(f in 1:length(filelist)){
  
  #Declare some tables for data
  Read.Data <- data.frame()
  Positive <- data.frame()  
  
  
  #This line reads the .txt file and places it into a table we can look at
  setwd(path.ano)
  filelist_ano_name <- gsub(" Detections", "", filelist[f])
  Read.Data.ano <- read.table(filelist_ano_name, header = T, sep="\t", fill = TRUE)
  #Read.Dataano <- subset(Read.Dataano, Read.Dataano$Name == "PathAnnotationObject" & Read.Dataano$Area.µm.2 > 0)
  
  setwd(path.det)
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  
  Read.Data[is.na(Read.Data)] <- 0
  Read.Data.ano[is.na(Read.Data.ano)] <- 0
  #Basic calculations from the data, Negatives are all the things that are given the class Negative in the data etc, can be changed to be whatever
  
  
  for(regionName in unique(Read.Data$Parent)){
    if(regionName == 'Cerebellum' | regionName == 'Cortex'| regionName == 'Hippocampus'| regionName == 'Hypothalamus'| regionName == 'Thalamus' ){
      
      Negative <- subset(Read.Data, Read.Data$Parent == regionName & Read.Data$Class == "negative")
      Low <- subset(Read.Data, Read.Data$Parent == regionName & Read.Data$Class == "low")
      Medium <- subset(Read.Data, Read.Data$Parent == regionName & Read.Data$Class == "medium")
      High <- subset(Read.Data, Read.Data$Parent == regionName & Read.Data$Class == "high")
      NegativeArea <- sum(Negative$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
      LowArea <- sum(Low$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
      MediumArea <- sum(Medium$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
      HighArea <- sum(High$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
      #cellArea <- NegativeArea+PositiveArea
      
      #Set annotation names here if there are any specific ROIs
      realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == regionName)
      anoArea <- sum(realAnnotations$Area.Âµm.2) / 1000000
      
      #Set channel to record intensity here
      Negative_MeanIntensity <- mean(Negative$DAB..Nucleus..Mean)
      Low_MeanIntensity <- mean(Low$DAB..Nucleus..Mean)
      Medium_MeanIntensity <- mean(Medium$DAB..Nucleus..Mean)
      High_MeanIntensity <- mean(High$DAB..Nucleus..Mean)
      
      
      Tot.Cells <- nrow(Low) + nrow(Medium) + nrow(High)  + nrow(Negative)
      #This DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
      #so k,1, if k = 1, would go in the first row, first column etc...
      
      filename <- gsub(".txt", "", filelist[f])
      
      Sample <- gsub(".mrxs Detections.txt", "", filelist[f])
      
      DataDraft[k,1] <- Sample
      DataDraft[k,2] <- regionName
      
      DataDraft[k,3] <- nrow(Low) / anoArea 
      DataDraft[k,4] <- nrow(Low)
      DataDraft[k,5] <- nrow(Low) / (Tot.Cells) 
      DataDraft[k,6] <- Low_MeanIntensity
      DataDraft[k,7] <- LowArea
      DataDraft[k,8] <- nrow(Medium) / anoArea
      DataDraft[k,9] <- nrow(Medium)
      DataDraft[k,10] <- nrow(Medium) / (Tot.Cells) 
      DataDraft[k,11] <- Medium_MeanIntensity
      DataDraft[k,12] <- MediumArea
      DataDraft[k,13] <- nrow(High) / anoArea
      DataDraft[k,14] <- nrow(High)
      DataDraft[k,15] <- nrow(High) / (Tot.Cells) 
      DataDraft[k,16] <- High_MeanIntensity
      DataDraft[k,17] <- HighArea
      DataDraft[k,18] <- nrow(Negative) / anoArea
      DataDraft[k,19] <- nrow(Negative)
      DataDraft[k,20] <- nrow(Negative) / (Tot.Cells) 
      DataDraft[k,21] <- Negative_MeanIntensity
      DataDraft[k,22] <- NegativeArea
      DataDraft[k,23] <- anoArea
      DataDraft[k,24] <- (Tot.Cells)
      
      print(paste('completed', filelist[f], regionName))
      #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
      k = k + 1
    } #else {
    print(paste('skipped', filelist[f], regionName))
    
  }
}


colnames(DataDraft) <- c("Sample", 
                         "Section",
                         
                         "Low - Cell Density (cells/mm^2)",
                         "Low - Cell Count", 
                         "Low - Cell %",
                         "Low - Nucleus Intensity",
                         "Low - Cell Area (mm^2)",
                         "Med - Cell Density (cells/mm^2)",
                         "Med - Cell Count", 
                         "Med - Cell %",
                         "Med - Nucleus Intensity",
                         "Med - Cell Area (mm^2)",
                         "High - Cell Density (cells/mm^2)",
                         "High - Cell Count", 
                         "High - Cell %",
                         "High - Nucleus Intensity",
                         "High - Cell Area (mm^2)",
                         "Negative - Cell Density (cells/mm^2)",
                         "Negative - Cell Count", 
                         "Negative - Cell %",
                         "Negative - Nucleus Intensity",
                         "Negative - Cell Area (mm^2)", 
                         "Annotation Area (mm^2)",
                         "Total Cell Count")

)


write.csv(DataDraft,paste("Data_BinnedbyRegion",k,".csv"), row.names=FALSE)
