//RandomRegion = getAnnotationObjects().findAll{it.getPathClass() == getPathClass("Fold")}
//RandomRegion.each{anno->
//    CellsinRandomRegion = getCurrentHierarchy().getObjectsForROI(qupath.lib.objects.PathDetectionObject, anno.getROI())
//}
//CellsinRandomRegion.each{cell->
//    getCurrentHierarchy().getSelectionModel().setSelectedObject(cell, true);
//}
////clearSelectedObjects()
//
////Delete annotation by class
//selectObjectsByClassification("Fold");
//clearSelectedObjects(true);
//clearSelectedObjects();

// Find and delete objects classified as "Fold" in an annotation

def annotationObjects = getAnnotationObjects().findAll { it.getPathClass() == getPathClass("Fold") }

annotationObjects.each { annotation ->
    def cellsInAnnotation = getCurrentHierarchy().getObjectsForROI(PathObject, annotation.getROI())
    cellsInAnnotation.each { cell ->
        getCurrentHierarchy().getSelectionModel().setSelectedObject(cell, true)
    }
}

// Clear the selected objects and delete the annotation
clearSelectedObjects(true)