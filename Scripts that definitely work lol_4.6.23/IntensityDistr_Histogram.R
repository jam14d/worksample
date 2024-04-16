#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-801 Rome_22-661 Rome_qp//detection results_12.2.22"
path.ano = "C://Analysis_Studies//22-801 Rome_22-661 Rome_qp//annotation results_12.2.22"
path.hist = "C://Analysis_Studies//22-801 Rome_22-661 Rome_qp//histo_test"
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
  
  
  NegativeArea <- sum(Negative$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  PositiveArea <- sum(Positive$Cell..Area) / 1000000 #division for conversion frum um^2 to mm^2
  
  #if IF, use Positive$Positive..Green.mean
  #if HDAB, use Positive$Positive..DAB.OD.mean
  
  Mean_Intensity <- mean(Positive$Nucleus..DAB.OD.mean)
  
  
  Quant_Intensity = quantile((Positive$Nucleus..DAB.OD.mean), c(.25,.5,.75))
  
  Min_Intensity <- min(Positive$Nucleus..DAB.OD.mean)
  Med_Intensity <- median(Positive$Nucleus..DAB.OD.mean)
  Max_Intensity <- max(Positive$Nucleus..DAB.OD.mean)
  
  Tot.Cells <- nrow(Positive) + nrow(Negative)
  
  filename_histo <- gsub(".mrxs Detections.txt", "", filelist[f])
  setwd(path.hist)
  jpeg(file=paste(filename_histo, "Intensity.jpg"))
  hist(Positive$Nucleus..DAB.OD.mean, main=paste(filename_histo, ": Intensity"), xlab="Cell Intensity Mean", xlim=c(0,0.5))
  dev.off()
  setwd(path.det)
  
  
  #ANNOTATIONSTUFF
  
  realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "PathAnnotationObject")
  # realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "Fat")
  anoArea <- sum(realAnnotations$Area.µm.2)/ 1000000 #division for conversion frum um^2 to mm^2
  
  #DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
  DataDraft[k,1] <- gsub(".mrxs.txt", "", filename)
  DataDraft[k,2] <- nrow(Positive) / anoArea
  DataDraft[k,3] <- nrow(Positive)
  DataDraft[k,4] <- nrow(Positive) / (nrow(Positive) + nrow(Negative))
  DataDraft[k,5] <- Mean_Intensity
  DataDraft[k,6] <- Min_Intensity
  DataDraft[k,7] <- Med_Intensity
  DataDraft[k,8] <- Max_Intensity
  DataDraft[k,9] <- Quant_Intensity[[1]] #lower 25th percentile
  DataDraft[k,10] <- Quant_Intensity[[2]] #50th percentile
  DataDraft[k,11] <- Quant_Intensity[[3]] #upper 75th percentile
  DataDraft[k,12] <- PositiveArea
  DataDraft[k,13] <- nrow(Negative)
  DataDraft[k,14] <- NegativeArea
  DataDraft[k,15] <- anoArea
  DataDraft[k,16] <- nrow(Positive) + nrow(Negative)
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}

colnames(DataDraft) <- c("Sample", 
                         "Positive Cell Density (Positives/mm^2)",
                         "Positive Cell Count", 
                         "Positive Cell %",
                         "Positive Cell Intensity - Overall",
                         "Min Intensity",
                         "Med Intensity", 
                         "Max Intensity",
                         "Lower 25th Percentile Intensity",
                         "50th Percentile Intensity",
                         "Upper 75th Percentile Intensity",
                         "Positive Area (mm^2)",
                         "Negative Cell Count", 
                         "Negative Cell Area (mm^2)", 
                         "Annotation Area (mm^2)",
                         "Total Cell Count")

#Writes a csv file with the data in the path
write.csv(DataDraft,paste("Data_test",f,".csv"))