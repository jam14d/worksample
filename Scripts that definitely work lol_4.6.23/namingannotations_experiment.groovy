resolveHierarchy()

def Hip = getPathClass("Hippocampus") 

int counter = 1
getAnnotationObjects().each { annotation ->
    if (annotation.getPathClass().equals(Hip))
        annotation.setName("A" + counter++)
}
print "Done!"     
       
def Cort = getPathClass("Cortex") 

getAnnotationObjects().each { annotation ->
    if (annotation.getPathClass().equals(Cort))
        annotation.setName("B" + counter++)
}
print "Done!"     

//rename annotations B4-B6.. eventually lol if i figure this out
