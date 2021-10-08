import sys
sys.path.append('..')
from tetra3 import Tetra3
from PIL import Image
from pathlib import Path

# Create instance
t3 = Tetra3()
# Generate and save database
t3.generate_database(max_fov=50, save_as='my_database_name')

# Path where images are
path = Path('../test_data/SOST')
for impath in path.glob('*.tiff'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        solved = t3.solve_from_image(img)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(solved))
