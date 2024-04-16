library("openxlsx")
library("stringr")

path = "C://Analysis_Studies//22-467 Boundless_Hscore_qp//detection_hscore_12.12.22"
setwd(path)

filelist <- dir(path,pattern = ".txt")

#for creating the final xlsx
wb <- createWorkbook()

for(f in 1:length(filelist)){
  print(filelist[f])
  filename <- gsub(".mrxs Detections.txt", "", filelist[f])
  DataDraft <- data.frame(matrix(ncol=28))
  
  
  colnames(DataDraft) <- c("Sample",
                           
                           "Positive Cell Count",
                           "Positive Cell Area (mm^2)",
                           
                           "Low Cell Density (cells/mm^2)",
                           "Low Cell Count",
                           "Low Cell Area (mm^2)",
                           "Low Cell %",
                           "Low Intensity",
                           
                           "Medium Cell Density (cells/mm^2)",
                           "Medium Cell Count",
                           "Medium Cell Area (mm^2)",
                           "Medium Cell %",
                           "Medium Intensity",
                           
                           "High Cell Density (cells/mm^2)",
                           "High Cell Count",
                           "High Cell Area (mm^2)",
                           "High Cell %",
                           "High Intensity",
                           
                           "Negative Cell Density (cells/mm^2)",
                           "Negative Cell Count",
                           "Negative Cell Area (mm^2)",
                           "Negative Cell %",
                           "Negative Intensity",
                           
                           "Total Cell Count",
                           "Total Cell Area (mm^2)",
                           
                           #These last 3 will be split off into the heatmap Excel sheets
                           "Letter",
                           "Number",
                           "Positive Cell Density: Pos Cell Count / Cell Area (Cells/mm^2)")
  
  k=1
  
  initialdata <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  initialdata[is.na(initialdata)] <- 0 #if any "NA" entries, make them "0"
  #testdata <- initialdata
  #initialdata$Name <- substr(initialdata$Name, 1, 4) #Takes names like "A-6 - Excluded" and makes them just "A-6"
  #initialdata <- subset(initialdata, substr(initialdata$Name, 2, 2) == "-") #gets rid of random annotations like "Junk", "Excluded", etc.
  
  
  
  for (name in unique(initialdata$TMA.core)){
    print(name)
    coredata <- subset(initialdata, initialdata$TMA.core == name)
    #Positive <- subset(coredata, coredata$Class == "Positive")
    #Negative <- subset(coredata, coredata$Class == "Negative")
    Negative <- subset(coredata, coredata$Class == "Tumor: Negative")
    Low <- subset(coredata, coredata$Class == "Tumor: 1+")
    Medium <- subset(coredata, coredata$Class == "Tumor: 2+")
    High <- subset(coredata, coredata$Class == "Tumor: 3+")
    
    totCellArea <- (sum(Low$Cell..Area) + sum(Medium$Cell..Area) + sum(High$Cell..Area) + sum(Negative$Cell..Area))/ 1000000
    
    DataDraft[k,1] <- name
    DataDraft[k,2] <- (nrow(Low) + nrow(Medium) + nrow(High))
    DataDraft[k,3] <- sum(sum(Low$Cell..Area),
                             sum(Medium$Cell..Area),
                             sum(High$Cell..Area),
                             sum(Negative$Cell..Area)) / 1000000
    DataDraft[k,4] <- nrow(Low) / totCellArea
    DataDraft[k,5] <- nrow(Low)
    DataDraft[k,6] <- sum(Low$Cell..Area) / 1000000
    DataDraft[k,7] <- nrow(Low) / (nrow(Low) + nrow(Medium) + nrow(High) + nrow(Negative))
    DataDraft[k,8] <- mean(Low$Nucleus..DAB.OD.mean)
    
    DataDraft[k,9] <- nrow(Medium) / totCellArea
    DataDraft[k,10] <- nrow(Medium)
    DataDraft[k,11] <- sum(Medium$Cell..Area) / 1000000
    DataDraft[k,12] <- nrow(Medium) / (nrow(Low) + nrow(Medium) + nrow(High) + nrow(Negative))
    DataDraft[k,13] <- mean(Medium$Nucleus..DAB.OD.mean)
    
    DataDraft[k,14] <- nrow(High) / totCellArea
    DataDraft[k,15] <- nrow(High)
    DataDraft[k,16] <- sum(High$Cell..Area) / 1000000
    DataDraft[k,17] <- nrow(High) / (nrow(Low) + nrow(Medium) + nrow(High) + nrow(Negative))
    DataDraft[k,18] <- mean(High$Nucleus..DAB.OD.mean)
    
    DataDraft[k,19] <- nrow(Negative) / totCellArea
    DataDraft[k,20] <- nrow(Negative)
    DataDraft[k,21] <- sum(Negative$Cell..Area) / 1000000
    DataDraft[k,22] <- nrow(Negative) / (nrow(Low) + nrow(Medium) + nrow(High) + nrow(Negative))
    DataDraft[k,23] <- mean(Negative$Nucleus..DAB.OD.mean)
    
    DataDraft[k,24] <- (nrow(Low) + nrow(Medium) + nrow(High) + nrow(Negative))
    DataDraft[k,25] <- totCellArea
    
    DataDraft[k,26] <- substr(name, 1, 1)
    DataDraft[k,27] <- strtoi(trimws(substr(name, 2, 3))) #convert to integer for ordering
    DataDraft[k,28] <- (nrow(Low) + nrow(Medium) + nrow(High)) / totCellArea
    
    k = k + 1
  }
  
  DataDraft <- DataDraft[order(DataDraft$Letter, DataDraft$Number),] #get the sheet in order by core
  
  #split off the HM data
  #HM <- DataDraft[, c("Letter", "Number",  "Positive Cell Density: Pos Cell Count / Cell Area (Cells/mm^2)")]
  FinalDraft <- DataDraft[,1:25]
  
  #filename <- gsub(".txt", "", filelist[f])
  #creating a workbook for the data (NOT Heatmaps, they need to be on their own)
  sheetname <- gsub("22-402 ", "", filename)
  
  addWorksheet(wb, sheetname)
  writeData(wb, sheetname, FinalDraft, startRow = 1, startCol = 1)
  
  write.csv(FinalDraft, paste("Data_hello", filename, ".csv"), row.names=FALSE)
  write.xlsx(HM, paste("HeatMap Data ", filename, ".xlsx"), row.names = FALSE) #needs to be xlsx format for the heatmap python script
  
  #write.csv(DataDraft,paste("TvS Total Data", filename, ".csv"), row.names=FALSE)
  print(filelist[f])
}
#write.csv(DataDraft,paste("DataTestingTesting123", k ," ", ".csv"))
saveWorkbook(wb, file = paste("22-467 Data", ".xlsx"), overwrite = TRUE)