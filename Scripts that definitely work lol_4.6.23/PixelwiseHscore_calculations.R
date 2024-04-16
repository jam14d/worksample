#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-1005 Biosplice_qp//detections_cell"
path.ano = "C://Analysis_Studies//22-1005 Biosplice_qp//annotations_cell"
#path.hist = "C://Analysis_Studies//22-801 Rome_22-661 Rome_qp//histogram data_12.2.22"
setwd(path.det)

#Tells it to look for all .txt files in the path given above
filelist <- dir(path.det,pattern = ".txt")

#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 16))

#This is a counter, set it equal to 1 outside of the for loop, within the for loop we increase it (k = k + 1) 
#through each pass through the loop to have a counter for each row of data, so first .txt file goes in k = 1 row, second is k = k + 1 row etc..
k = 1

#For loop, for every file ending in .txt in that path, we will run through this loop of calculations once.  
for(f in 1:length(filelist)){
  
  #Declare some tables for data
  Read.Data <- data.frame()
  Cell <- data.frame()  
  
  #This line reads the .txt file and places it into a table we can look at
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  
  setwd(path.ano)
  filename <- gsub(" Detections", "", filelist[f])
  Read.Data.ano <- read.table(filename, header=T, sep="\t", fill = TRUE)
  setwd(path.det)
  #Basic calculations from the data, Necrosiss are all the things that are given the class Necrosis in the data etc, can be changed to be whatever
  Necrosis <- subset(Read.Data, Read.Data$Class == "Necrosis")
  Cell <- subset(Read.Data, Read.Data$Class == "Cell")
  
  F
  NecrosisArea <- sum(Necrosis$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  CellArea <- sum(Cell$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  
  #if IF, use Cell$Cell..Green.mean
  #if HDAB, use Cell$Cell..DAB.OD.mean
  
  Mean_Intensity <- mean(Cell$Nucleus..DAB.OD.mean)
  
  
  Quant_Intensity = quantile((Cell$Nucleus..DAB.OD.mean), c(.25,.5,.75))
  
  Min_Intensity <- min(Cell$Nucleus..DAB.OD.mean)
  Med_Intensity <- median(Cell$Nucleus..DAB.OD.mean)
  Max_Intensity <- max(Cell$Nucleus..DAB.OD.mean)
  
  Tot.Cells <- nrow(Cell) + nrow(Necrosis)
  
  
  realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "PathAnnotationObject")
  # realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "Fat")
  anoArea <- sum(realAnnotations$Area.µm.2)/ 1000000 #division for conversion frum um^2 to mm^2
  
  #DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
  DataDraft[k,1] <- gsub(".mrxs.txt", "", filename)
  DataDraft[k,2] <- nrow(Cell) / anoArea
  DataDraft[k,3] <- nrow(Cell)
  DataDraft[k,4] <- nrow(Cell) / (nrow(Cell) + nrow(Necrosis))
  DataDraft[k,5] <- Mean_Intensity
  DataDraft[k,6] <- Min_Intensity
  DataDraft[k,7] <- Med_Intensity
  DataDraft[k,8] <- Max_Intensity
  DataDraft[k,9] <- Quant_Intensity[[1]] #lower 25th percentile
  DataDraft[k,10] <- Quant_Intensity[[2]] #50th percentile
  DataDraft[k,11] <- Quant_Intensity[[3]] #upper 75th percentile
  DataDraft[k,12] <- CellArea
  DataDraft[k,13] <- nrow(Necrosis)
  DataDraft[k,14] <- NecrosisArea
  DataDraft[k,15] <- anoArea
  DataDraft[k,16] <- nrow(Cell) + nrow(Necrosis)
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}

colnames(DataDraft) <- c("Sample", 
                         "Cell Cell Density (Cells/mm^2)",
                         "Cell Cell Count", 
                         "Cell Cell %",
                         "Cell Cell Intensity - Overall",
                         "Min Intensity",
                         "Med Intensity", 
                         "Max Intensity",
                         "Lower 25th Percentile Intensity",
                         "50th Percentile Intensity",
                         "Upper 75th Percentile Intensity",
                         "Cell Area (mm^2)",
                         "Necrosis Cell Count", 
                         "Necrosis Cell Area (mm^2)", 
                         "Annotation Area (mm^2)",
                         "Total Cell Count")

#Writes a csv file with the data in the path
write.csv(DataDraft,paste("Data_test",f,".csv"))