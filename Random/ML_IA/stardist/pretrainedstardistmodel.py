from stardist.models import StarDist2D

def list_available_models():
    """Prints a list of available pretrained models."""
    print("Available models:", StarDist2D.from_pretrained())

def load_pretrained_model(model_name='2D_versatile_fluo'):
    """Creates and returns a pretrained model."""
    model = StarDist2D.from_pretrained(model_name)
    return model

# List available pretrained models
list_available_models()

# Load a specific pretrained model
model = load_pretrained_model()
