import os
from config import *

import sys, os, math, random
from time import time
import numpy as np
from threading import *
import matplotlib.pyplot as plt
import matplotlib
from threading import Thread
import skimage.io as io
from skimage.transform import iradon, rescale, radon
from skimage import io
from skimage.data import shepp_logan_phantom
from scipy.optimize import minimize
from scipy.optimize import fmin
from natsort import natsorted
from PIL import Image


def ReSin(i):
	slicei = Image.open(DIR_SLICE+"\\slc_"+str(i)+".jpg")
	theta = np.linspace(0.0, 180.0,1440, endpoint=False)
	SliceSin = list()
	for j in theta:
		s = np.asarray(slicei.rotate(-j, fillcolor=slicei.getpixel((4, 4)), expand=False), dtype='uint8')
		#s = s[:,:,0] + s[:,:,1] + s[:,:,2]
		p = s.sum(axis=0)
		SliceSin.append(p)
	SliceSin = (np.array(SliceSin)/1440)/255
	#matplotlib.image.imsave("sls.jpg", SliceSin)
	plt.imsave("sls.jpg", np.asarray(SliceSin, dtype='uint8'))
	sin = np.array(Image.open(DIR_SIN+"\\s"+str(i)+".jpg"))
	#sin = sin[:,:,0] + sin[:,:,1] + sin[:,:,2]
	NewSin = sin + (SliceSin*255-sin)*K
	print("k")
	#matplotlib.image.imsave(DIR_SIN+"\\s"+str(i)+".jpg", NewSin/255)
	plt.imsave(DIR_SIN+"\\s"+str(i)+".jpg", np.asarray(NewSin, dtype='uint8'))
	return [np.mean((SliceSin-sin)), NewSin[:,:,0] + NewSin[:,:,1] + NewSin[:,:,2]]

def RecSlice(SliceDir, sin, i): ## recover one slice using sinogram array ##
	theta = np.linspace(0.0, 180.0,min(sin.shape), endpoint=False)
	rec = iradon(sin.transpose(), theta=theta, filter_name='shepp-logan')
	plt.imsave(SliceDir+"\\slc_"+str(i)+".jpg", rec, cmap = plt.cm.gray)

def IterateRec(islc):
	diff = 100
	while abs(diff)>10:
		diff = ReSin(islc)[0]
		sin = ReSin(islc)[1]
		RecSlice(DIR_SLICE, 2*sin, islc)
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

# comment for or if	
'''
if USE_CALIBR_ITERATE==True:
	print("Iterative method is started.")
	for i in  REC_ISLICE:
		thi = Thread(target=IterateRec, args=[i])
		thi.start()
'''
