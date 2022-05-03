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
t3 = Tetra3('default_database')

# Path where images are
import csv
file = open('solution_12_deg_tetra3.csv', 'w')
csv_cols = ['Image', 'RA', 'Dec', 'Roll', 'FOV', 'RMSE', 'Matches', 'Prob', 'T_solve', 'T_extract']
writer = csv.DictWriter(file, fieldnames=csv_cols)
writer.writeheader()

path = Path('../test_data/Actual Images/GI1.png')
for impath in path.glob('*.png'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        solved = t3.solve_from_image(img)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(solved))
    im_name = {'Image': str(impath)}
    solved.update(im_name)

    for value in [solved]:
        writer.writerow(value)

file.close()
