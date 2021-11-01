# Script to view .fits images
import numpy as np
import astropy

import matplotlib
import matplotlib.pyplot as plt

import sys
sys.path.append('..')
import tetra3
#from tetra3 import Tetra3
from PIL import Image
from pathlib import Path

from astropy.io import fits
image_file = ('../test_data/leoobj/2018-10-15_19_35_02_843248.fits') # put image filename here, must end in .fits

image_data = fits.getdata(image_file)
print(type(image_data))
print(image_data.shape)

# Crop image to fit FOV; these images are 108 deg diagonal FOV
image_cropped = tetra3.crop_and_downsample_image(image_data, crop=8, downsample=None, sum_when_downsample=True, return_offsets=False)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance

plt.imshow(image_cropped, cmap='gray')
plt.colorbar()
plt.show()

print(type(image_cropped))
print(image_cropped.shape)
