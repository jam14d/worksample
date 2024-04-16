library(openxlsx)
library(data.table)
library(stringr)

##this is the script for 21-841 ribon
#Change path here, this is where your data is
path.det = "C://Analysis_Studies//22-187 Ribon QP//detections_asthma"
path.ano = "C://Analysis_Studies//22-187 Ribon QP//annotations_asthma"

setwd(path.det)

#Tells it to look for all .txt files in the path given above
#filelist_raw <- dir(path.det,pattern = ".txt") #Need this janky code because QP2 exports the detections files with "Detections" after the .mrxs extension...
#filelist_int <- strsplit(filelist_raw, " Detections")
#filelist <- unlist(filelist_int)[2*(1:length(filelist_raw))-1]
filelist <- dir(path.det,pattern = ".txt")


#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 12))

#Qupath colors (may not match native image colors)
QPRed = "PARP14" #QP Red
QPGreen = "CD3" #QP Green
QPYellow = "CD68" #QP Yellow

#QP string names
##had to separate into diff versions of same category because janky composite
cell_name = "FITC_Negative: Cy5_Negative: TRITC_Negative"
cell_name_2 = "FITC_Background: Cy5_Negative: TRITC_Negative"
cell_name_3 = "FITC_Background: Cy5_Negative: TRITC_Background"
FITC_posName = "FITC: Cy5_Negative: TRITC_Negative"
FITC_posName_2 = "FITC: Cy5_Negative: TRITC_Background"
Cy5_posName = "FITC_Negative: Cy5: TRITC_Negative"
Cy5_posName_2 = "FITC_Background: Cy5: TRITC_Background"
TRITC_posName = "FITC_Negative: Cy5_Negative: TRITC"
TRITC_posName_2 = "FITC_Background: Cy5_Negative: TRITC"
double_positive = "FITC: Cy5: TRITC_Negative"
double_positive_2 = "FITC_Negative: Cy5: TRITC"

#This is a counter, set it equal to 1 outside of the for loop, within the for loop we increase it (k = k + 1) 
#through each pass through the loop to have a counter for each row of data, so first .txt file goes in k = 1 row, second is k = k + 1 row etc..

k = 1

#For loop, for every file ending in .txt in that path, we will run through this loop of calculations once.  
for(f in 1:length(filelist)){
  
  #Declare some tables for data
  Read.Data <- data.frame()
  Negative <- data.frame()
  
  #This line reads the .txt file and places it into a table we can look at
  
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  setwd(path.ano)
  filename <- gsub(" Detections", "", filelist[f])
  Read.Data.ano <- read.table(filename, header=T, sep="\t", fill = TRUE)
  setwd(path.det)
  
  #Here we subset based off strings within the Name column
  QPred_only <- subset(Read.Data, Read.Data$Name == Cy5_posName| Read.Data$Name == Cy5_posName_2)
  QPgreen_only <- subset(Read.Data, Read.Data$Name == FITC_posName | Read.Data$Name == FITC_posName_2)
  QPyellow_only <- subset(Read.Data, Read.Data$Name == TRITC_posName| Read.Data$Name == TRITC_posName_2)
  QPboth <- subset(Read.Data, Read.Data$Name == double_positive)
  QPboth_2 <- subset(Read.Data, Read.Data$Name == double_positive_2)
  QPneg <- subset(Read.Data, Read.Data$Name == cell_name | Read.Data$Name == cell_name_2 | Read.Data$Name == cell_name_3)
  QPred_all <- subset(Read.Data, Read.Data$Name == Cy5_posName | Read.Data$Name == double_positive | Read.Data$Name == double_positive_2)
  QPgreen_all <- subset(Read.Data, Read.Data$Name == FITC_posName | Read.Data$Name == double_positive)
  QPyellow_all <- subset(Read.Data, Read.Data$Name == TRITC_posName | Read.Data$Name == double_positive_2)
  
  #Basic calculations from the data, Negatives are all the things that are given the class Negative in the data etc, can be changed to be whatever
  
  
  NegativeArea <- sum(QPneg$Cell..Area.µm.2) / 1000000
  posRedArea <- sum(QPred_all$Cell..Area.µm.2) / 1000000
  posGreenArea <- sum(QPgreen_all$Cell..Area.µm.2) / 1000000
  posYellowArea <- sum(QPyellow_all$Cell..Area.µm.2) / 1000000
  posBothArea <- sum(QPboth$Cell..Area.µm.2) / 1000000
  posBothArea_2 <- sum(QPboth_2$Cell..Area.µm.2) / 1000000
  totalCellArea <- NegativeArea+posRedArea+posGreenArea+posYellowArea+posBothArea+posBothArea_2
  realAnnotations <- subset(Read.Data.ano, Read.Data.ano$Name == "Tissue" | Read.Data.ano$Name == "PathAnnotationObject")
  anoArea <- sum(realAnnotations$Area.µm.2) / 1000000
  
  redIntensity <- mean(QPred_all$Opal.690..Cell..Mean)
  greenIntensity<-mean(QPgreen_all$Opal.520..Cell..Mean)
  yellowIntensity<-mean(QPyellow_all$Opal.570..Cell..Mean)
  
  totalCells <- nrow(QPred_only) + nrow(QPgreen_only) + nrow(QPyellow_only) + nrow(QPboth) + nrow(QPboth_2) + nrow(QPneg)
  
  #This DataDraft is the table where all of the calculations go from before, the brackets indicate the coordinate of where that calculation goes
  #so k,1, if k = 1, would go in the first row, first column etc...
  
  filename <- gsub(".txt", "", filelist[f])
  filename <- gsub(".mrxs", "", filelist[f])
  
  DataDraft[k,1] <- filename
  
  DataDraft[k,2] <- nrow(QPgreen_all) / anoArea
  DataDraft[k,3] <- nrow(QPgreen_all)
  DataDraft[k,4] <- posGreenArea
  DataDraft[k,5] <- nrow(QPgreen_all) / totalCells
  DataDraft[k,6] <- greenIntensity
  
  DataDraft[k,7] <- nrow(QPred_all) / anoArea
  DataDraft[k,8] <- nrow(QPred_all)
  DataDraft[k,9] <- posRedArea
  DataDraft[k,10] <- nrow(QPred_all) / totalCells
  DataDraft[k,11] <- redIntensity
  
  DataDraft[k,12] <- nrow(QPyellow_all) / anoArea
  DataDraft[k,13] <- nrow(QPyellow_all)
  DataDraft[k,14] <- posYellowArea
  DataDraft[k,15] <- nrow(QPyellow_all) / totalCells
  DataDraft[k,16] <- yellowIntensity
  
  
  DataDraft[k,17] <- nrow(QPboth) / anoArea
  DataDraft[k,18] <- nrow(QPboth)
  DataDraft[k,19] <- posBothArea 
  DataDraft[k,20] <- nrow(QPboth) / totalCells
  
  DataDraft[k,21] <- nrow(QPboth_2) / anoArea
  DataDraft[k,22] <- nrow(QPboth_2)
  DataDraft[k,23] <- posBothArea_2
  DataDraft[k,24] <- nrow(QPboth_2) / totalCells
  
  DataDraft[k,25] <- totalCells
  DataDraft[k,26] <- totalCellArea
  DataDraft[k,27] <- anoArea
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}
Marker1 <- QPGreen
Marker2 <- QPRed
Marker3 <- QPYellow
colnames(DataDraft) <- c("Sample", 
                         "Marker1 + / Marker2 - Cell Density (cells/mm^2)",
                         "Marker1 + / Marker2 - Cell Count",
                         "Marker1 + / Marker2 - Cell Area (mm^2)",
                         "Marker1 + / Marker2 - Cell Percentage", 
                         "Marker1 + / Marker2 - Intensity",
                         
                         "Marker1 - / Marker2 + Cell Density (cells/mm^2)",
                         "Marker1 - / Marker2 + Cell Count",
                         "Marker1 - / Marker2 + Cell Area (mm^2)",
                         "Marker1 - / Marker2 + Cell Percentage", 
                         "Marker1 - / Marker2 + Intensity",
                         
                         "Marker3 + / Marker2 - Cell Density (cells/mm^2)",
                         "Marker3 + / Marker2 - Cell Count",
                         "Marker3 + / Marker2 - Cell Area (mm^2)",
                         "Marker3 + / Marker2 - Cell Percentage", 
                         "Marker3 + / Marker2 - Intensity",
                         
                         "Marker1 + / Marker2 + Cell Density (cells/mm^2)",
                         "Marker1 + / Marker2 + Cell Count",
                         "Marker1 + / Marker2 + Cell Area (mm^2)",
                         "Marker1 + / Marker2 + Cell Percentage", 
                         
                         "Marker3 + / Marker2 + Cell Density (cells/mm^2)",
                         "Marker3 + / Marker2 + Cell Count",
                         "Marker3 + / Marker2 + Cell Area (mm^2)",
                         "Marker3 + / Marker2 + Cell Percentage", 
                         
                         "Total Cell Count",
                         "Total Cell Area (mm^2)",
                         "Total Annotation Area (mm^2)")



#Writes a csv file with the data in the path
write.csv(DataDraft,paste("IF Data_5.8.23",f,".csv"), row.names = F)
write.xlsx(DataDraft, paste("IF Data Excel_5.8.23",f,".xlsx")) #excel files make for easier formatting

print(paste("DONE! csv written to", getwd())) 