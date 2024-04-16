import com.google.gson.Gson
import qupath.lib.geom.Point2
import qupath.lib.objects.PathAnnotationObject
import qupath.lib.roi.PolygonROI
//SAVE YOUR QP FILE BEFORE RUNNING!!!

// write all class names that should be exported to jsons. 
// if annotations/detections are not classed, set terms = ["null"] to export all annotations
out_dir = 'exported_shapes_22-183'
//terms = ["null"]
terms = ["A1", "A2", "B1", "B2"] 
shape = 'Annotations'

def imageData = QPEx.getCurrentImageData()
def imageName = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
print(imageName)

def pathOutput = buildFilePath(PROJECT_BASE_DIR, out_dir)
mkdirs(pathOutput)
def filename = buildFilePath(PROJECT_BASE_DIR, out_dir, imageName + '.json')
def file = new File(filename)
file.delete() 

//bounds are the buffer space used by QP in displaying mrxs images
double dx = getCurrentServer().boundsX
double dy = getCurrentServer().boundsY

//This will translate the annotation on the slide to correct for how QP displays mrxs files
if (shape == 'Annotations'){
    translated_anos = getAnnotationObjects().findAll({p -> (p.getPathClass().toString() in terms)})
    }

if (shape == 'Detections'){
    translated_anos = getDetectionObjects().findAll({p -> (p.getPathClass().toString() in terms)})
    }

// translate shapes to 
tranlated_anos = translated_anos.each({it.ROI = it.ROI.translate(dx, dy)})

boolean prettyPrint = true
def gson = GsonTools.getInstance(prettyPrint)
file << gson.toJson(translated_anos) << System.lineSeparator()
print("Export DONE!")

// this will replace your annotation/detections after exporting their translated cooridnates
translated_anos = translated_anos.each({it.ROI = it.ROI.translate(-dx, -dy)})
//last edited July 6th 2022 -SL