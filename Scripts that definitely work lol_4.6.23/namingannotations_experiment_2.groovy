resolveHierarchy()
int counter = 1
for (var ann: getAnnotationObjects()) {
    if (ann.getParent() != null && ann.getParent().getName() == "sectionA")
        ann.setName(counter++)
    if (ann.getParent() != null && ann.getParent().getName() == "sectionB")
        ann.setName(counter++)
    if (ann.getParent() != null && ann.getParent().getName() == "sectionC")
        ann.setName(counter++)
    
}

def anns = getAnnotationObjects().findAll { 
    if (it.getName() == null)
        return false
    return it.getName().startsWith("section") 
}
getCurrentHierarchy().removeObjects(anns, true)