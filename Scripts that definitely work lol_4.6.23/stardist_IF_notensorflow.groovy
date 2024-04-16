

//runtiles
//selectAnnotations();
//runPlugin('qupath.lib.algorithms.TilerPlugin', '{"tileSizeMicrons": 2000.0,  "trimToROI": true,  "makeAnnotations": false,  "removeParentAnnotation": false}');


import qupath.ext.stardist.StarDist2D

// Specify the model file (you will need to change this!)
var pathModel = "C:/Users/analysis_a/ImageAnalysisCode/reference_code/qupath_groovy/Stardist/dsb2018_heavy_augment.pb"

var stardist = StarDist2D.builder(pathModel)
        .threshold(0.4)              // Probability (detection) threshold
        .channels('DAPI')            // Specify detection channel
        .normalizePercentiles(1, 99) // Percentile normalization
        .pixelSize(0.4)              // Resolution for detection
        .cellExpansion(5.0)          // Approximate cells based upon nucleus expansion
        //.cellConstrainScale(1.5)     // Constrain cell expansion using nucleus size
        .measureShape()              // Add shape measurements
        .measureIntensity()          // Add cell measurements (in all compartments)
        .build()
        

// Run detection for the selected objects
var imageData = getCurrentImageData()
selectAnnotations()
var pathObjects = getSelectedObjects()
if (pathObjects.isEmpty()) {
    Dialogs.showErrorMessage("StarDist", "Please select a parent object!")
    return
}
stardist.detectObjects(imageData, pathObjects)
println 'Done!'