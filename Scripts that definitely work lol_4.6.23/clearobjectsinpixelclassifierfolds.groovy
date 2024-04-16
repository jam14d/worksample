import qupath.lib.objects.PathObject

//clear objects within an annotation created froms a pixel classifier, classed "Fold"

//create annotations from pixel classifier
selectAnnotations();
createAnnotationsFromPixelClassifier("fold", 1000.0, 0.0, "SPLIT")
resetSelection()

//find the annotations, which are classed as "Fold"
def annotationObjects = getAnnotationObjects().findAll { it.getPathClass() == getPathClass("Fold") }


//grab objects within the annotation
annotationObjects.each { annotation ->
    def roi = annotation.getROI()
    def cellsInAnnotation = getCurrentHierarchy().getObjectsForROI(PathObject, roi)

    cellsInAnnotation.each { cell ->
        getCurrentHierarchy().getSelectionModel().setSelectedObject(cell, true)
    }
}

//clear those objects
clearSelectedObjects(true)
clearSelectedObjects()