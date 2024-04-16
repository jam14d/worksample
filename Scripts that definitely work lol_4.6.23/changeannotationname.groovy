def newClass = getPathClass(null)   // Your new class here
def oldClass = getPathClass("Positive")

getAnnotationObjects().each { annotation ->
    if (annotation.getPathClass().equals(oldClass))
        annotation.setPathClass(newClass)
}
//fireHierarchyUpdate() // If you want to update the count in the Annotation pane

print "Done!"