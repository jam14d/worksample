import qupath.lib.roi.RectangleROI
import qupath.lib.objects.PathAnnotationObject

// Size in pixels at the base resolution
int size = 5000

// Get center pixel
def viewer = getCurrentViewer()
int cx = viewer.getCenterPixelX()
int cy = viewer.getCenterPixelY()

// Create & add annotation
def roi = new RectangleROI(cx-size/2, cy-size/2, size, size)
def annotation = new PathAnnotationObject(roi)
addObject(annotation)