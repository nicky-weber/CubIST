# tetra3.Tetra3 # class to solve images & load/create databases
# tetra3.get_centroids_from_image()# extract spot centroids
# tetra3.crop_and_downsample_image()# crop/downsample image
#
# use tetra3 code to solve
import sys
sys.path.append('..')
from tetra3_tracking import Tetra3
from PIL import Image
from pathlib import Path
import numpy as np
# Create instance and load default_database (built with max_fov=12 and the rest as default)
t3 = Tetra3('default_database')
def crop_and_downsample_image(image, crop=None, downsample=None, sum_when_downsample=True,
                              return_offsets=False):
    """Crop and/or downsample an image. Cropping is applied before downsampling.

    Args:
        image (numpy.ndarray): The image to crop and downsample. Must be 2D.
        crop (int or tuple, optional): Desired cropping of the image. May be defined in three ways:

            - Scalar: Image is cropped to given fraction (e.g. crop=2 gives 1/2 size image out).
            - 2-tuple: Image is cropped to centered region with size crop = (height, width).
            - 4-tuple: Image is cropped to region with size crop[0:2] = (height, width), offset
              from the centre by crop[2:4] = (offset_down, offset_right).

        downsample (int, optional): Downsampling factor, e.g. downsample=2 will combine 2x2 pixel
            regions into one. The image width and height must be divisible by this factor.
        sum_when_downsample (bool, optional): If True (the default) downsampled pixels are
            calculated by summing the original pixel values. If False the mean is used.
        return_offsets (bool, optional): If True, return the applied cropping offset.
    Returns:
        numpy.ndarray or tuple: If `return_offsets=False` (the default) a 2D array with the cropped
        and dowsampled image is returned. If `return_offsets=True` is passed a tuple containing
        the image and a tuple with the cropping offsets (top, left) is returned.
    """
    # Input must be 2-d numpy array
    # Crop can be either a scalar, 2-tuple, or 4-tuple:
    # Scalar: Image is cropped to given fraction (eg input crop=2 gives 1/2 size image out)
    # If 2-tuple: Image is cropped to center region with size crop = (height, width)
    # If 4-tuple: Image is cropped to ROI with size crop[0:1] = (height, width)
    #             offset from centre by crop[2:3] = (offset_down, offset_right)
    # Downsample is made by summing regions of downsample by downsample pixels.
    # To get the mean set sum_when_downsample=False.
    # Returned array is same type as input array!

    image = np.asarray(image)
    assert image.ndim == 2, 'Input must be 2D'
    # Do nothing if both are None
    if crop is None and downsample is None:
        if return_offsets is True:
            return (image, (0, 0))
        else:
            return image
    full_height, full_width = image.shape
    # Check if input is integer type (and therefore can overflow...)
    if np.issubdtype(image.dtype, np.integer):
        intype = image.dtype
    else:
        intype = None
    # Crop:
    if crop is not None:
        try:
            # Make crop into list of int
            crop = [int(x) for x in crop]
            if len(crop) == 2:
                crop = crop + [0, 0]
            elif len(crop) == 4:
                pass
            else:
                raise ValueError('Length of crop must be 2 or 4 if iterable, not '
                                 + str(len(crop)) + '.')
        except TypeError:
            # Could not make list (i.e. not iterable input), crop to portion
            crop = int(crop)
            assert crop > 0, 'Crop must be greater than zero if scalar.'
            assert full_height % crop == 0 and full_width % crop == 0,\
                'Crop must be divisor of image height and width if scalar.'
            crop = [full_height // crop, full_width // crop, 0, 0]
        # Calculate new height and width (making sure divisible with future downsampling)
        divisor = downsample if downsample is not None else 2
        height = int(np.ceil(crop[0]/divisor)*divisor)
        width = int(np.ceil(crop[1]/divisor)*divisor)
        # Clamp at original size
        if height > full_height:
            height = full_height
        if width > full_width:
            width = full_width
        # Calculate offsets from centre
        offs_h = int(round(crop[2] + (full_height - height)/2))
        offs_w = int(round(crop[3] + (full_width - width)/2))
        # Clamp to be inside original image
        if offs_h < 0:
            offs_h = 0
        if offs_h > full_height-height:
            offs_h = full_height-height
        if offs_w < 0:
            offs_w = 0
        if offs_w > full_width-width:
            offs_w = full_width-width
        # Do the cropping
        image = image[offs_h:offs_h+height, offs_w:offs_w+width]
    else:
        offs_h = 0
        offs_w = 0
        height = full_height
        width = full_width
    # Downsample:
    if downsample is not None:
        assert height % downsample == 0 and width % downsample == 0,\
            '(Cropped) image must be divisible by downsampling factor'
        if intype is not None:
            # Convert integer types into float for summing without overflow risk
            image = image.astype(np.float32)
        if sum_when_downsample is True:
            image = image.reshape((height//downsample, downsample, width//downsample,
                                   downsample)).sum(axis=-1).sum(axis=1)
        else:
            image = image.reshape((height//downsample, downsample, width//downsample,
                                   downsample)).mean(axis=-1).mean(axis=1)
        if intype is not None:
            # Convert back with clipping
            image = image.clip(np.iinfo(intype).min, np.iinfo(intype).max).astype(intype)
    # Return image and if desired the offset.
    if return_offsets is True:
        return (image, (offs_h, offs_w))
    else:
        return image
# Path where images are
path = Path('../test_data/Downsample - 2/')
for impath in path.glob('*.tiff'):
    print('Solving for image at: ' + str(impath))
    with Image.open(str(impath)) as img:
        img=crop_and_downsample_image(img,crop=None, downsample=2)
        solved = t3.solve_from_image(img, crop=None, downsample=None)#, fov_estimate=11.4, fov_max_error=0.1)  # Adding e.g. fov_estimate=11.4, fov_max_error=.1 improves performance
    print('Solution: ' + str(list(solved.items())[:-1]))
   # print('solved:'+str(solved))
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

    solved = t3.solve_from_image_tracking(img,slew_rate_bound=2,time_for_last_solution=t_tot/1000,star_centroids_last=star_centroids)
    #print('Solution Tracking: ',str(solved))2
    print('Solution Tracking: ' + str(list(solved.items())[:-1]))
