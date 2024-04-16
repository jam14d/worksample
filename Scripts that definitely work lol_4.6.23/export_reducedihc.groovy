def entry = getProjectEntry()
def name = entry.getImageName() + '.txt'

def path = buildFilePath(PROJECT_BASE_DIR, 'annotation results')
mkdirs(path)
path = buildFilePath(path, name)
saveAnnotationMeasurements(path, 'Name', 'ROI', 'Centroid X µm', 'Centroid Y µm', 'Area µm^2')

def path2 = buildFilePath(PROJECT_BASE_DIR, 'detection results')
mkdirs(path2)
path = buildFilePath(path2, name)
saveDetectionMeasurements(path2, 'Class', 'Centroid X µm', 'Centroid Y µm', 'Cell: Area µm^2', 'DAB: Cell: Mean')

print 'Results exported to ' + path