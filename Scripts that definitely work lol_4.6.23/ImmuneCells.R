#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-214 Ohio State University_qp//detections_1"
path.ano = "C://Analysis_Studies//22-214 Ohio State University_qp//annotations_1"
setwd(path.det)


#Tells it to look for all .txt files in the path given above
filelist <- dir(path.det,pattern = ".txt")

#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 7))

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
  sample <- gsub(".mrxs.txt", "", filename)
  Read.Data.ano <- read.table(filename, header=T, sep="\t", fill = TRUE)
  setwd(path.det)
  #Basic calculations from the data, Negatives are all the things that are given the class Negative in the data etc, can be changed to be whatever
  
  Negative <- subset(Read.Data, Read.Data$Class == "Other")
  Positive <- subset(Read.Data, Read.Data$Class == "Positive")
  
  NegativeArea <- sum(Negative$Area.µm.2) / 1000000
  PositiveArea <- sum(Positive$Area.µm.2) / 1000000
  
  Tot.Cells <- nrow(Positive) + nrow(Negative)
  realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "PathAnnotationObject")
  anoArea <- sum(realAnnotations$Area.µm.2) / 1000000
  #This DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
  #so k,1, if k = 1, would go in the first row, first column etc...
  
  DataDraft[k,1] <- sample
  DataDraft[k,2] <- nrow(Positive) / anoArea
  DataDraft[k,3] <- nrow(Positive)
  DataDraft[k,4] <- (nrow(Positive) / Tot.Cells) * 100
  DataDraft[k,5] <- PositiveArea  
  DataDraft[k,6] <- Tot.Cells
  DataDraft[k,7] <- anoArea
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}

colnames(DataDraft) <- c("Sample", 
                         "Immune Cell Density (cells/mm^2)",
                         "Immune Cell Count", 
                         "Immune Cell %",
                         "Total Immune Cell Area (mm^2)", 
                         "Total Cell Count", 
                         "Annotation Area (mm^2)")

#Writes a csv file with the data in the path
write.csv(DataDraft,paste("Data",f,".csv"))









