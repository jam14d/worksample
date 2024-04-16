// QP 0.2.3
AREA_THRESHOLD = 57256

def server = getCurrentServer()
def pixelWidth = server.getMetadata().getPixelCalibration()getPixelWidthMicrons()
def pixelHeight = server.getMetadata().getPixelCalibration()getPixelHeightMicrons()

def smallAnnotations = getAnnotationObjects().findAll {it.getROI().getScaledArea(pixelWidth, pixelHeight) < AREA_THRESHOLD}
removeObjects(smallAnnotations, true)