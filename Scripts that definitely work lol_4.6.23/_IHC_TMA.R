library("openxlsx")
library("stringr")

path = "C://Analysis_Studies//22-467 Boundless_qp//detection_ESC1502"
setwd(path)

filelist <- dir(path,pattern = ".txt")

#for creating the final xlsx
wb <- createWorkbook()

for(f in 1:length(filelist)){
  print(filelist[f])
  filename <- gsub(".mrxs Detections.txt", "", filelist[f])
  DataDraft <- data.frame(matrix(ncol=13))
  
  
  colnames(DataDraft) <- c("Sample",
                           
                           "Positive Cell Density (cells/mm^2)",
                           "Positive Cell Count",
                           "Positive Cell Area (mm^2)",
                           "Positive Cell %",
                           "Positive Intensity",
                           
                           "Negative Cell Count",
                           "Negative Cell Area",
                           
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
    Positive <- subset(coredata, coredata$Class == "Positive")
    Negative <- subset(coredata, coredata$Class == "Negative")
    
    totCellArea <- (sum(Positive$Cell..Area) + sum(Negative$Cell..Area))/ 1000000
    
    DataDraft[k,1] <- name
    DataDraft[k,2] <- nrow(Positive) / totCellArea
    
    DataDraft[k,3] <- nrow(Positive)
    DataDraft[k,4] <- sum(Positive$Cell..Area) / 1000000
    DataDraft[k,5] <- nrow(Positive) / (nrow(Positive) + nrow(Negative))
    DataDraft[k,6] <- mean(Positive$Nucleus..0.50.µm.per.pixel..DAB..Mean)
    DataDraft[k,7] <- nrow(Negative)
    DataDraft[k,8] <- sum(Negative$Cell..Area) / 1000000
    
    DataDraft[k,9] <- (nrow(Positive) + nrow(Negative))
    DataDraft[k,10] <- totCellArea
    
    DataDraft[k,11] <- substr(name, 1, 1)
    DataDraft[k,12] <- strtoi(trimws(substr(name, 3, 4))) #convert to int for ordering
    DataDraft[k,13] <- nrow(Positive) / totCellArea
    
    k = k + 1
  }
  
  DataDraft <- DataDraft[order(DataDraft$Letter, DataDraft$Number),] #get the sheet in order by core
  
  #split off the HM data
  HM <- DataDraft[, c("Letter", "Number",  "Positive Cell Density: Pos Cell Count / Cell Area (Cells/mm^2)")]
  FinalDraft <- DataDraft[,1:10]
  
  #filename <- gsub(".txt", "", filelist[f])
  #creating a workbook for the data (NOT Heatmaps, they need to be on their own)
  sheetname <- gsub("22-402 ", "", filename)
  
  addWorksheet(wb, sheetname)
  writeData(wb, sheetname, FinalDraft, startRow = 1, startCol = 1)
  
  write.csv(FinalDraft, paste("Data", filename, ".csv"), row.names=FALSE)
  write.xlsx(HM, paste("HeatMap Data ", filename, ".xlsx"), row.names = FALSE) #needs to be xlsx format for the heatmap python script
  
  write.csv(DataDraft,paste("TvS Total Data", filename, ".csv"), row.names=FALSE)
  print(filelist[f])
}
#write.csv(DataDraft,paste("DataTestingTesting123", k ," ", ".csv"))
saveWorkbook(wb, file = paste("22-402 Data", ".xlsx"), overwrite = TRUE)