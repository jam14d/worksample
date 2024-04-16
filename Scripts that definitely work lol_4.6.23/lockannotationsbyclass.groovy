selectObjects(p -> p.isAnnotation() == true && p.getPathClass() == getPathClass("DRG"))
getSelectedObjects().each{it.setLocked(true)}