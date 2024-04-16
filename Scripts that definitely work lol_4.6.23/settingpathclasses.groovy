//def A = getPathClass('A')
def Center = getPathClass('Center')
getAnnotationObjects().eachWithIndex { annotation , i ->
   if (i == 2)
      annotation.setPathClass(Center)
//  else
//      annotation.setPathClass(A)
}
//fireHierarchyUpdate()