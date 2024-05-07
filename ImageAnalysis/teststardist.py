from stardist.data import test_image_nuclei_2d
from stardist.plot import render_label
from csbdeep.utils import normalize
import matplotlib.pyplot as plt

def load_test_image():
    """Loads a test image from the StarDist dataset."""
    return test_image_nuclei_2d()

def predict_and_plot(model):
    """Uses the provided model to predict and plot the image with overlays."""
    img = load_test_image()
    labels, _ = model.predict_instances(normalize(img))

    plt.figure(figsize=(10, 5))
    plt.subplot(1,2,1)
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.title("Input Image")

    plt.subplot(1,2,2)
    plt.imshow(render_label(labels, img=img))
    plt.axis("off")
    plt.title("Prediction + Input Overlay")

    plt.show()

# Assuming the model is defined elsewhere and imported here
from pretrainedstardistmodel import model  # Adjust this import as per your actual file/module setup

# Use the model to predict and plot
predict_and_plot(model)

#pip install certifi
#export SSL_CERT_FILE=$(python -m certifi)
#python /Users/jamieannemortel/Projects/ImageAnalysis/test_model.py
