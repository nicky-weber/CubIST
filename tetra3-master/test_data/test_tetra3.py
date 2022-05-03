"""
This example loads the tetra3 default database and solves for every image in the tetra3/test_data directory.

Note: Requires PIL (pip install Pillow)
"""
import sys
sys.path.append('..')
from tetra3 import Tetra3
from PIL import Image
from pathlib import Path

# Create instance and load default_database (built with max_fov=12 and the rest as default)
t3 = Tetra3('7')

# Path where images are
path = Path('../test_data/Actual Images/Bortle4_Vail_3-13-2022')
for impath in path.glob('*.bmp'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        solved = t3.solve_from_image(img, crop=None, downsample=None)#, fov_estimate=11.4, fov_max_error=0.1)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(solved))
