##FINAL SCRIPT - 

#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-214 Ohio State University_qp//detections_byregion"
path.ano = "C://Analysis_Studies//22-214 Ohio State University_qp//annotations_byregion"

setwd(path.ano)
filelistano <- sort(dir(path.ano,pattern = ".txt"))

setwd(path.det)
filelist <- sort(dir(path.det,pattern = ".txt"))

#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 15))

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
  #Read.Dataano <- subset(Read.Dataano, Read.Dataano$Name == "PathAnnotationObject" & Read.Dataano$Area.�m.2 > 0)
  
  setwd(path.det)
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  
  Read.Data[is.na(Read.Data)] <- 0
  Read.Data.ano[is.na(Read.Data.ano)] <- 0
  #Basic calculations from the data, Negatives are all the things that are given the class Negative in the data etc, can be changed to be whatever
  
  
  for(regionName in unique(Read.Data$Parent)){
    if(regionName == 'A' | regionName == 'B'| regionName == 'C' ){
      
      Negative <- subset(Read.Data, Read.Data$Parent == regionName & Read.Data$Class == "Other")
      Positive <- subset(Read.Data, Read.Data$Parent == regionName & Read.Data$Class == "Positive")
      NegativeArea <- sum(Negative$Area.µm.2) / 1000000 #sums all cell areas and converts from um^2 to mm^2
      PositiveArea <- sum(Positive$Area.µm.2) / 1000000 #sums all cell areas and converts from um^2 to mm^2
      cellArea <- NegativeArea+PositiveArea
      
      #Set annotation names here if there are any specific ROIs
      realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == regionName)
      anoArea <- sum(realAnnotations$Area.µm.2) / 1000000
      
      #Set channel to record intensity here
      Intensity <- mean(Positive$Nucleus..Hematoxylin.OD.mean)
      
      
      totCellArea <- (NegativeArea + PositiveArea)
      #This DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
      #so k,1, if k = 1, would go in the first row, first column etc...
      
      filename <- gsub(".txt", "", filelist[f])
      
      Sample <- gsub(".mrxs Detections.txt", "", filelist[f])
      
      DataDraft[k,1] <- Sample
      DataDraft[k,2] <- regionName
      
      DataDraft[k,3] <- nrow(Positive) / anoArea
      DataDraft[k,4] <- nrow(Positive)
      DataDraft[k,5] <- sum(Positive$Area.µm.2) / 1000000
      DataDraft[k,6] <- (nrow(Positive) / (nrow(Positive) + nrow(Negative))) * 100
      DataDraft[k,7] <- (nrow(Positive) + nrow(Negative))
      DataDraft[k,8] <- anoArea
      
      print(paste('completed', filelist[f], regionName))
      #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
      k = k + 1
    } #else {
    print(paste('skipped', filelist[f], regionName))
    
  }
}


colnames(DataDraft) <- c("Sample", 
                         "Section",
                         
                         "Immune Cell Density (cells/mm^2)",
                         "Immune Cell Count",
                         "Immune Cell Area (mm^2)",
                         "Immune Cell %",
                         
                         "Total Cell Count",
                         "Annotation Area"
)


write.csv(DataDraft,paste("Data",k,".csv"), row.names=FALSE)