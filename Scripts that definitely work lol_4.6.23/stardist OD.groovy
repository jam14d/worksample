//clear detections
//clearDetections();

//run tiles
//selectAnnotations();
runPlugin('qupath.lib.algorithms.TilerPlugin', '{"tileSizeMicrons": 3000.0,  "trimToROI": true,  "makeAnnotations": true,  "removeParentAnnotation": true}');

//runstardist_OD
import qupath.ext.stardist.StarDist2D
import static qupath.lib.gui.scripting.QPEx.*

// Specify the model directory (you will need to change this!)
def pathModel = "C:/Program Files/QuPath-0.3/stardist_files/dsb2018_heavy_augment.pb"

def imageData = getCurrentImageData()
def stains = imageData.getColorDeconvolutionStains()
clearDetections();

def stardist = StarDist2D.builder(pathModel)
        .preprocess(
            ImageOps.Channels.deconvolve(stains),
            ImageOps.Channels.extract(0,1),
            ImageOps.Channels.sum(),
            ImageOps.Filters.median(2),
            ImageOps.Core.divide(2)
         ) 
        .threshold(0.05)               // Prediction threshold
        .normalizePercentiles(1, 99) // Percentile normalization
        .pixelSize(0.2423)              // Resolution for detection
        .cellExpansion(5.0)          // Approximate cells based upon nucleus expansion
        .measureShape()              // Add shape measurements
        .measureIntensity()          // Add cell measurements (in all compartments)
        .build()

// Run detection for the selected objects

selectAnnotations();
def pathObjects = getSelectedObjects()
for (o in pathObjects) {
    detections = stardist.detectObjects(imageData, o.getROI())
    addObjects(detections)
    println 'Done!'
    
    javafx.application.Platform.runLater {
    getCurrentViewer().getImageRegionStore().cache.clear()
    System.gc()
    }
}

// Select then merge annotations
selectAnnotations();
mergeSelectedAnnotations()


