#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-1005 Biosplice_qp//detections_cell"
path.ano = "C://Analysis_Studies//22-1005 Biosplice_qp//annotations_cell"
setwd(path.det)

#Tells it to look for all .txt files in the path given above
filelist <- dir(path.det,pattern = ".txt")

#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 22))

#This is a counter, set it equal to 1 outside of the for loop, within the for loop we increase it (k = k + 1) 
#through each pass through the loop to have a counter for each row of data, so first .txt file goes in k = 1 row, second is k = k + 1 row etc..
k = 1

#For loop, for every file ending in .txt in that path, we will run through this loop of calculations once.  
for(f in 1:length(filelist)){
  
  #Declare some tables for data
  Read.Data <- data.frame()
  Positive <- data.frame()  
  
  #This line reads the .txt file and places it into a table we can look at
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  
  setwd(path.ano)
  filename <- gsub(" Detections", "", filelist[f])
  Read.Data.ano <- read.table(filename, header=T, sep="\t", fill = TRUE)
  setwd(path.det)
  #Basic calculations from the data, Negatives are all the things that are given the class Negative in the data etc, can be changed to be whatever
  Negative <- subset(Read.Data, Read.Data$Class == "Negative")
  Positive <- subset(Read.Data, Read.Data$Class == "Positive")
  
  Positive_Low_Intensity <- subset(Positive, Positive$Cell..DAB.OD.mean < 0.1)
  Positive_Med_Intensity <- subset(Positive, Positive$Cell..DAB.OD.mean >= 0.1 & Positive$Cell..DAB.OD.mean <= 0.2)
  Positive_High_Intensity <- subset(Positive, Positive$Cell..DAB.OD.mean > 0.2)
  
  NegativeArea <- sum(Negative$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  PositiveArea <- sum(Positive$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  
  #if IF, use Positive$Cell..Green.mean
  #if HDAB, use Positive$Cell..DAB.OD.mean
  Mean_Intensity <- mean(Positive$Cell..DAB.OD.mean)
  
  Low_Intensity <- mean(Positive_Low_Intensity$Cell..DAB.OD.mean)
  Med_Intensity <- mean(Positive_Med_Intensity$Cell..DAB.OD.mean)
  High_Intensity <- mean(Positive_High_Intensity$Cell..DAB.OD.mean)
  
  Tot.Cells <- nrow(Positive) + nrow(Negative)
  realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "PathAnnotationObject")
  # realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "Fat")
  anoArea <- sum(realAnnotations$Area.µm.2)/ 1000000 #division for conversion frum um^2 to mm^2
  
  #DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
  DataDraft[k,1] <- gsub(".mrxs.txt", "", filename)
  DataDraft[k,2] <- nrow(Positive) / anoArea
  DataDraft[k,3] <- nrow(Positive)
  DataDraft[k,4] <- nrow(Positive) / (nrow(Positive) + nrow(Negative))
  DataDraft[k,5] <- Mean_Intensity
  DataDraft[k,6] <- nrow(Positive_Low_Intensity) / anoArea
  DataDraft[k,7] <- nrow(Positive_Low_Intensity)
  DataDraft[k,8] <- nrow(Positive_Low_Intensity) / (nrow(Positive) + nrow(Negative))
  DataDraft[k,9] <- nrow(Positive_Med_Intensity) / anoArea
  DataDraft[k,10] <- nrow(Positive_Med_Intensity)
  DataDraft[k,11] <- nrow(Positive_Med_Intensity) / (nrow(Positive) + nrow(Negative))
  DataDraft[k,12] <- nrow(Positive_High_Intensity) / anoArea
  DataDraft[k,13] <- nrow(Positive_High_Intensity)
  DataDraft[k,14] <- nrow(Positive_High_Intensity) / (nrow(Positive) + nrow(Negative))
  DataDraft[k,15] <- Low_Intensity
  DataDraft[k,16] <- Med_Intensity
  DataDraft[k,17] <- High_Intensity
  DataDraft[k,18] <- PositiveArea
  DataDraft[k,19] <- nrow(Negative)
  DataDraft[k,20] <- NegativeArea
  DataDraft[k,21] <- anoArea
  DataDraft[k,22] <- nrow(Positive) + nrow(Negative)
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}

colnames(DataDraft) <- c("Sample", 
                         "Positive Cell Density (cells/mm^2)",
                         "Positive Cell Count", 
                         "Positive Cell %",
                         "Positive Cell Intensity - Overall",
                         "Positive Cell Density (cells/mm^2) - Low Bin",
                         "Positive Cell Count - Low Bin", 
                         "Positive Cell % - Low Bin",
                         "Positive Cell Density (cells/mm^2) - Med Bin",
                         "Positive Cell Count - Med Bin", 
                         "Positive Cell % - Med Bin",
                         "Positive Cell Density (cells/mm^2) - High Bin",
                         "Positive Cell Count - High Bin", 
                         "Positive Cell % - High Bin",
                         "Positive Cell Intensity - Low Bin",
                         "Positive Cell Intensity - Med Bin",
                         "Positive Cell Intensity - High Bin",
                         "Positive Cell Area (mm^2)",
                         "Negative Cell Count", 
                         "Negative Cell Area (mm^2)", 
                         "Annotation Area (mm^2)",
                         "Total Cell Count")

#Writes a csv file with the data in the path
write.csv(DataDraft,paste("Data_7.19.22_new",f,".csv"))