import os
from config import *

import sys, os, math, random
from time import time
import numpy as np
from threading import *
import matplotlib.pyplot as plt
from threading import Thread
import skimage.io as io
from skimage.transform import iradon, rescale, radon
from skimage import io
from skimage.data import shepp_logan_phantom
from scipy.optimize import minimize
from scipy.optimize import fmin
from natsort import natsorted
from PIL import Image

def RecSlice(SliceDir, sin, i): ## recover one slice using sinogram array ##
	theta = np.linspace(0.0, 180.0,min(sin.shape), endpoint=False)
	rec = iradon(sin.transpose(), theta=theta, filter_name='shepp-logan')
	plt.imsave(SliceDir+"\\slc_"+str(i)+".jpg", rec, cmap = plt.cm.gray)
		
if os.path.isdir(DIR_SLICE+"\\")==False:
	print("Create directory with slices at " + DIR_SLICE + ".")
	os.mkdir(DIR_SLICE)

print ("Loading sinograms...")
img = list()
for i in  REC_ISLICE:
	p = np.array(Image.open(DIR_SIN+"\\s"+str(i)+".jpg"))[:,:,0]
	img.append(p)
print("Done.")
print ("Reconstruction is started...", end="\r")
print(end = "\n")
k=0
for i in  REC_ISLICE:
	th = Thread(target=RecSlice, args=(DIR_SLICE, img[k], i))
	th.start()
	k += 1
