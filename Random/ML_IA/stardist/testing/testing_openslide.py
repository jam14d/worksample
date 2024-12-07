import sys
print("Python EXE:", sys.executable)
print("Python version:", sys.version)
import site
print("Site-packages location:", site.getsitepackages())
import openslide

try:
    slide = openslide.OpenSlide('/Users/jamieannemortel/Downloads/CMU-1.tiff')
    print(slide.properties)
    slide.close()
except Exception as e:
    print("Error:", e)



#nano ~/.zshrc

#export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/opt/homebrew/Cellar/openslide/4.0.0/lib
