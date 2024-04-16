def min_nuc_area=14 //remove any nuclei with an area less than this (in microns)
nuc_area_measurement='Cell: Area µm^2'
def toDelete = getDetectionObjects().findAll {measurement(it, nuc_area_measurement) <= min_nuc_area}
removeObjects(toDelete, true)