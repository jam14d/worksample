selectAnnotations();
def Class = getPathClass('A')


selected = getSelectedObjects()
for (def annotation in selected){
annotation.setPathClass(Class)
}
fireHierarchyUpdate()
println("Done!")