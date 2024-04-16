#Change path here, this is where your data is
#Writes a csv file with the data in the path

#The data was acquired by running the export script on "Live" Images
#So have the positive pixel class you are happy with running Live and viewable
#Give it a second to load
#Then run the export
#Repeat for each slide 

path.ano = "C://Analysis_Studies//23-472 UC Davis_qp//annotations_pixelclassifier"

setwd(path.ano)
#Tells it to look for all .txt files in the path given above
filelist <- dir(path.ano,pattern = ".txt")


#Makes the final summary table with 12 columns with those column headers in order, these can be changed if needed
DataDraft <- data.frame(matrix(ncol = 6))

#This is a counter, set it equal to 1 outside of the for loop, within the for loop we increase it (k = k + 1) 
#through each pass through the loop to have a counter for each row of data, so first .txt file goes in k = 1 row, second is k = k + 1 row etc..

k = 1

#For loop, for every file ending in .txt in that path, we will run through this loop of calculations once.  
for(f in 1:length(filelist)){
  filename = gsub(".mrxs.txt", "", filelist[f])
  
  #Declare some tables for data
  Read.Data <- data.frame()
  
  #This line reads the .txt file and places it into a table we can look at
  Read.Data <- read.table(filelist[f], header=T, sep="\t", fill = TRUE)
  
  
  positive_area_mm <- sum(Read.Data$PositiveArea_2..Positive.area.µm.2) / 1000000

  annotation_area <- sum(Read.Data$Area.µm.2) / 1000000
  negative_area_mm <- annotation_area - positive_area_mm
  
  DataDraft[k,1] <- filename
  DataDraft[k,2] <- positive_area_mm 
  DataDraft[k,3] <- (positive_area_mm / annotation_area) * 100
  DataDraft[k,4] <- negative_area_mm 
  DataDraft[k,5] <- (negative_area_mm / annotation_area) * 100
  DataDraft[k,6] <- annotation_area
  
  
  print(filelist[f])
  
  #The counter from before, k = k + 1, so essentially looking above we move to the next row in the table after one loop
  k = k + 1
}

colnames(DataDraft) <- c("Sample", 
                         "Positive Area (mm^2)",
                         "Positive Area Percentage (%)", #cell counts per total cell area
                         "Negative Area (mm^2)",
                         "Negative Area Percentage (%)",
                         "Total Area Analyzed (mm^2)")

write.csv(DataDraft,paste("Data",f,".csv"), row.names = FALSE)

