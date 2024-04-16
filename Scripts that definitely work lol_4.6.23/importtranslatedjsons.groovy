// Update the JSON_DIR variable below to the path where your annotation json files are stored
// The script will retrieve the current image name and load the annotations
// from the json with an identical name. This assumes your jsons are named: "image_name.json"

JSON_DIR = "C:/Analysis_Studies/23-159 Grace_DRG_qp/951998078_new"

// default TRANSLATE to false, 
// set to true if annotations are misaligned
TRANSLATE = false

def imageData = QPEx.getCurrentImageData()
def imageName = GeneralTools.getNameWithoutExtension(imageData.getServer().getMetadata().getName())
print(imageName)

def filename = buildFilePath(JSON_DIR, imageName + '.json')
def gson = GsonTools.getInstance(true)
def json = new File(filename).text

// Read the annotations
double dx = getCurrentServer().boundsX
double dy = getCurrentServer().boundsY
def type = new com.google.gson.reflect.TypeToken<List<qupath.lib.objects.PathObject>>() {}.getType()
def deserializedAnnotations = gson.fromJson(json, type)

if (TRANSLATE){
    translated_anos = deserializedAnnotations.each{it.ROI = it.ROI.translate(-dx, -dy)}
    addObjects(translated_anos)
    }
else{
    addObjects(deserializedAnnotations)
    }   

// last update: 5 Jan 2023 -SL