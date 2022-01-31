# tetra3.Tetra3 # class to solve images & load/create databases
# tetra3.get_centroids_from_image()# extract spot centroids
# tetra3.crop_and_downsample_image()# crop/downsample image
#
# use tetra3 code to solve
import sys
sys.path.append('..')
from tetra3_tracking_downsample import Tetra3, crop_and_downsample_image
from PIL import Image
from pathlib import Path
import numpy as np
# Create instance and load default_database (built with max_fov=12 and the rest as default)
t3 = Tetra3('default_database')

# Path where images are
path = Path('../test_data/Tracking/')
for impath in path.glob('*.png'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        # img = crop_and_downsample_image(img,crop=None,downsample=None)
        solved = t3.solve_from_image(img, crop=None, downsample=None)#, fov_estimate=11.4, fov_max_error=0.1)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(list(solved.items())[:-1]))
    
    sol=list(solved.items())
    # extract centroids and organize into array
    centroids=sol[-1]
    centroids=centroids[1:]
    centroids=str(centroids)
    centroids=centroids[2:-3]
    # remove punctuation
    punc = '[],'
    # Removing punctuations in string
    # Using loop + punctuation string
    for i in centroids:
        if i in punc:
            centroids = centroids.replace(i, "")
    # put in list
    star_centroids = centroids.split()
    # extract total time from 'solved' variable
    t_solve=sol[7]
    t_solve=str(t_solve[1:])
    t_solve=float(t_solve[1:-2])
    t_extract=sol[8]
    t_extract=str(t_extract[1:])
    t_extract=float(t_extract[1:-2])
    t_tot=t_solve+t_extract# total time

for impath in path.glob('*tracking.jpg'):
    print('Solving for image at: ' + str(impath))
    solved = t3.solve_from_image_tracking(img,slew_rate_bound=2,time_for_last_solution=t_tot/1000,star_centroids_last=star_centroids)
    print('Solution Tracking: ' + str(list(solved.items())[:-1]))
