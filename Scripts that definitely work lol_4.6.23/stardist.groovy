import qupath.ext.stardist.StarDist2D
import qupath.lib.images.servers.*
// Specify the model directory (you will need to change this!)
def pathModel = 'C:/Program Files/QuPath-0.3/stardist_files/he_heavy_augment.pb/'
//runPlugin('qupath.imagej.detect.tissue.SimpleTissueDetection2', '{"threshold": 240,  "requestedPixelSizeMicrons": 20.0,  "minAreaMicrons": 100000.0,  "maxHoleAreaMicrons": 1000000.0,  "darkBackground": false,  "smoothImage": true,  "medianCleanup": true,  "dilateBoundaries": false,  "smoothCoordinates": true,  "excludeOnBoundary": false,  "singleAnnotation": false}');
def stardist = StarDist2D.builder(pathModel)
      .threshold(0.3)              // Prediction threshold
      .normalizePercentiles(1, 99) // Percentile normalization
      .pixelSize(0.2423)              // Resolution for detection
      .cellExpansion(5.0)
      .measureShape()              // Add shape measurements
      .measureIntensity()
      .build()
def imageData = getCurrentImageData()
    annotations = getAnnotationObjects()
    for (annotation in annotations) {
        selectObjects(annotation)
        //selectAnnotations()
        def pathObjects = getSelectedObjects()
        if (pathObjects.isEmpty()) {
              Dialogs.showErrorMessage("StarDist", "Please select a parent object!")
              return
        }
        stardist.detectObjects(imageData, pathObjects)
        javafx.application.Platform.runLater {
            getCurrentViewer().getImageRegionStore().cache.clear()
            System.gc()
        }
    }
println 'Done!'

