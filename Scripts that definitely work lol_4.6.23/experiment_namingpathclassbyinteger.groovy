//resolveHierarchy()
def MarginA = getPathClass('A1')
def MarginB = getPathClass('B1')
def CenterA = getPathClass('A2')
def CenterB = getPathClass('B2')
def WholeTissue = getPathClass('A')
getAnnotationObjects().eachWithIndex { annotation , i ->
   if (i == 0)
      annotation.setPathClass(MarginA)
   if (i == 1)
      annotation.setPathClass(MarginB)
   if (i == 2)
     annotation.setPathClass(MarginB)
   if (i == 3)
      annotation.setPathClass(CenterA)
   if (i == 4)
      annotation.setPathClass(CenterB)

//  else
//      annotation.setPathClass(A)
}