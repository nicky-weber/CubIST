import sys
sys.path.append('..')
from tetra3 import Tetra3
from PIL import Image
from pathlib import Path

# Create instance
t3 = Tetra3()
# Generate and save database
t3.generate_database(max_fov=12, save_as='my_database_name')

t3 = Tetra3('my_database_name');

# Path where images are
import csv
file = open('solution_' + str(max_fov) + '_deg_tetra3.csv', 'w')
csv_cols = ['Image', 'RA', 'Dec', 'Roll', 'FOV', 'RMSE', 'Matches', 'Prob', 'T_solve', 'T_extract']
writer = csv.DictWriter(file, fieldnames=csv_cols)
writer.writeheader()

path = Path('../test_data/')
for impath in path.glob('*.tiff'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        solved = t3.solve_from_image(img)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(solved))
    im_name = {'Image': str(impath)}
    solved.update(im_name)

    for value in [solved]:
        writer.writerow(value)

file.close()
