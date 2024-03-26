# Image Analysis Sandbox

### A Note

There's a bunch of janky code in here. Many projects are still half-finished.

### Conda Environment Setup

I prefer using Conda for managing dependencies—it keeps things neat and tidy. If you haven't got Conda, the [official Conda documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) is a great place to start.

Create and activate a new Conda environment named `IA` with:

```
conda create --name IA python=3.8
conda activate IA
```

### Installing Dependencies
With the environment ready, install the necessary packages using pip. Here's what you'll need for most projects:

```
pip3 install matplotlib scikit-image tensorflow stardist --no-binary stardist --no-cache-dir
```

### Running Streamlit Applications
```
streamlit run your_app.py
```
