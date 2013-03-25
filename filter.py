import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io
import glob

from PIL import Image
from datetime import datetime

#as needed for debugging
from IPython.core.debugger import Tracer; debug_here = Tracer()

######################################
### CONFIGURATION/CALIBRATION DATA ###
######################################

INPREFIX='/Users/aron/Desktop/experiment/DSC_'
OUTPREFIX='/Users/aron/Desktop/experiment/'

# Set these as needed by examining an individual frame
# some helpful commands

#filename='/Users/aron/Desktop/experiment/DSC_1400.JPG'
#x = io.imread(filename)
#imshow(x)
#set IMIN->PMAX from image data
#RG_THRESHOLD and GREEN_THRESHOLD come from image background
#then check/validate
#from filter import process_frame
#process_frame(filename)

# y
IMIN =407
IMAX =2119

# x
JMIN =1788
JMAX =1967

PMIN = 1.0
PMAX = 9.0

RG_THRESHOLD = 10
BG_THRESHOLD = 20
GREEN_THRESHOLD = 100

#####################################
### END CALIBRATION/CONFIGURATION ###
#####################################

### CONSTANTS

EXIF_TIME_FORMAT = '%Y:%m:%d %H:%M:%S'
RED   = 0
GREEN = 1
BLUE  = 2

def get_exif_datetime(filename):
    img = Image.open(filename)
    exif_date = img._getexif()[306]
    return datetime.strptime(exif_date, EXIF_TIME_FORMAT)

def process_frame(filepath):
    uncropped_img = io.imread(filepath)
    img = uncropped_img[IMIN:IMAX,JMIN:JMAX,:]

    mask  = (img[:,:,GREEN] - RG_THRESHOLD > img[:,:,RED]) * \
            (img[:,:,GREEN] - BG_THRESHOLD > img[:,:,BLUE]) *\
            (img[:,:,GREEN] > GREEN_THRESHOLD)
    mask_i, mask_j = mask.nonzero()

    pressure_measure_in_pixels = (IMAX-min(mask_i))-IMIN
    frame_height_in_pixels = IMAX-IMIN
    frame_height_in_cm = PMAX-PMIN
    pixels_to_cm = frame_height_in_cm/frame_height_in_pixels

    pressure_measure_in_cm = pressure_measure_in_pixels*pixels_to_cm \
                                  + PMIN

    filename = os.path.split(filepath)[-1]
    io.imsave(OUTPREFIX+'cropped_'+filename,img)

    #good debugging spot for checking output
    #debug_here()

    return pressure_measure_in_cm

def process_dir():
    frames = glob.glob(INPREFIX + '*')
    framecount = len(frames)
    pressure = np.empty(framecount)
    time = np.empty(framecount)
    idx = 0

    frame0 = frames[0]
    starttime = get_exif_datetime(frame0)
    filename = os.path.split(frame0)[-1]
    img = io.imread(frame0)
    io.imsave(OUTPREFIX+'reference_'+filename,img)
    del img

    for frame in frames:
        pressure[idx] = process_frame(frame)
        time_delta = get_exif_datetime(frame) - starttime
        time[idx] = time_delta.total_seconds()
        print "frame: %d, pressure: %e, s: %d" % \
            (idx, pressure[idx], time[idx])
        idx = idx + 1
    return time, pressure

if __name__ == '__main__':
    time, pressure = process_dir()

    import pylab
    plt.plot(time,pressure)

#    filename='/Users/aron/Desktop/experiment/DSC_1423.JPG'
#    pressure_cm = process_frame(filename)
#    date = get_exif_datetime(filename)
