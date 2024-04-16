##normalized above 0.03 intensity - 22-404 Biosplice reanalysis


#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-710 Biosplice_qp//detection results_8.29.22"
path.ano = "C://Analysis_Studies//22-710 Biosplice_qp//annotation results_8.29.22"
setwd(path.det)

#Tells it to look for all .txt files in the path given above
filelist <- dir(path.det,pattern = ".txt")

#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 11))

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
  
  Positive_Normalized <- subset(Positive, Positive$Cell..DAB.OD.mean >= 0.04)
  
  Negative_Normalized <- subset(Negative, Negative$Cell..DAB.OD.mean < 0.04)
  
  NegativeNorm_Area <- sum(Negative_Normalized$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  PositiveNorm_Area <- sum(Positive_Normalized$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  
  #if IF, use Positive$Cell..Green.mean
  #if HDAB, use Positive$Cell..DAB.OD.mean
 
  PositiveNorm_MeanIntensity <- mean(Positive_Normalized$Cell..DAB.OD.mean)
  NegativeNorm_MeanIntensity <- mean(Negative_Normalized$Cell..DAB.OD.mean)
  
  Tot.Cells <- nrow(Positive) + nrow(Negative)
  realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "PathAnnotationObject")
  # realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "Fat")
  anoArea <- sum(realAnnotations$Area.µm.2)/ 1000000 #division for conversion frum um^2 to mm^2
  
  #DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
  DataDraft[k,1] <- gsub(".mrxs.txt", "", filename)
  DataDraft[k,2] <- nrow(Positive_Normalized) / anoArea
  DataDraft[k,3] <- nrow(Positive_Normalized)
  DataDraft[k,4] <- nrow(Positive_Normalized) / (nrow(Positive_Normalized) + nrow(Negative_Normalized))
  DataDraft[k,5] <- PositiveNorm_MeanIntensity
  DataDraft[k,6] <- PositiveNorm_Area
  DataDraft[k,7] <- nrow(Negative_Normalized)
  DataDraft[k,8] <- NegativeNorm_Area
  DataDraft[k,9] <- NegativeNorm_MeanIntensity
  DataDraft[k,10] <- anoArea
  DataDraft[k,11] <- nrow(Positive_Normalized) + nrow(Negative_Normalized)
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}

colnames(DataDraft) <- c("Sample", 
                         "Positive Cell Density (cells/mm^2)",
                         "Positive Cell Count", 
                         "Positive Cell %",
                         "Positive Cell Intensity",
                         "Positive Cell Area (mm^2)",
                         "Negative Cell Count", 
                         "Negative Cell Area (mm^2)",
                         "Negative Cell Intensity", 
                         "Annotation Area (mm^2)",
                         "Total Cell Count")

#Writes a csv file with the data in the path
write.csv(DataDraft,paste("Data_8.11.22",f,".csv"))

