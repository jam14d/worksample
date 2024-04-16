badParentName = "White Blob"

toRemove = getDetectionObjects().findAll{it.getParent().toString().contains(badParentName)}
removeObjects(toRemove, true)