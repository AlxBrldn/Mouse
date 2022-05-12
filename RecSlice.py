import os
from config import *

import sys, os, math, random
from time import time
from time import sleep
import numpy as np
from threading import *
import matplotlib.pyplot as plt
import matplotlib
from threading import Thread
import threading as thd
import skimage.io as io
from skimage.transform import iradon, rescale, radon
from skimage import io
from skimage.data import shepp_logan_phantom
#from scipy.optimize import minimize
#from scipy.optimize import fmin
from natsort import natsorted
from PIL import Image


def ReSin(i):
	slicei = Image.open(DIR_SLICE+"\\slc_"+str(i)+".bmp")
	theta = np.linspace(0.0, 180.0,1440, endpoint=False)
	SliceSin = list()
	for j in theta:
		s = np.asarray(slicei.rotate(-j, fillcolor=slicei.getpixel((4, 4)), expand=False), dtype='uint8')
		#s = s[:,:,0] + s[:,:,1] + s[:,:,2]
		p = s.sum(axis=0)
		SliceSin.append(p)
	SliceSin = (np.array(SliceSin)/1440)
	#matplotlib.image.imsave("sls.jpg", SliceSin)
	plt.imsave("sls.bmp", np.asarray(SliceSin, dtype='uint8'))
	sin = np.array(Image.open(DIR_SIN+"\\s"+str(i)+".bmp"))
	#sin = sin[:,:,0] + sin[:,:,1] + sin[:,:,2]
	NewSin = sin + (SliceSin-sin)*K
	#print("k")
	#matplotlib.image.imsave(DIR_SIN+"\\s"+str(i)+".jpg", NewSin/255)
	plt.imsave(DIR_SIN+"\\s"+str(i)+".bmp", np.asarray(NewSin, dtype='uint8'))
	return [np.mean((SliceSin-sin)), NewSin[:,:,0] + NewSin[:,:,1] + NewSin[:,:,2]]

def RecSlice(SliceDir, sin, i): ## recover one slice using sinogram array ##
	theta = np.linspace(0.0, 180.0,min(sin.shape), endpoint=False)
	rec = iradon(sin.transpose(), theta=theta, filter_name='shepp-logan')
	plt.imsave(SliceDir+"\\slc_"+str(i)+".bmp", rec, cmap = plt.cm.gray)

def IterateRec(islc):
	diff = 200
	while abs(diff)>ERR*180/100:
		diff = ReSin(islc)[0]
		print("ERR: ", round(diff*100/180, 1), end="%\r")
		sin = ReSin(islc)[1]
		RecSlice(DIR_SLICE, 2*sin, islc)
if os.path.isdir(DIR_SLICE+"\\")==False:
	print("Create directory with slices at " + DIR_SLICE + ".")
	os.mkdir(DIR_SLICE)

print ("Loading sinograms...")
img = list()
for i in  REC_ISLICE:
	p = np.array(Image.open(DIR_SIN+"\\s"+str(i)+".bmp"))[:,:,0]
	img.append(p)
print("Done.")
print ("Reconstruction is started...", end="\r")
print(end = "\n")

k=0
for i in  REC_ISLICE:
	th = Thread(target=RecSlice, args=(DIR_SLICE, img[k], i))
	th.start()
	k += 1	

while(thd.active_count()!=1):
	sleep(1)
if USE_CALIBR_ITERATE==True and thd.active_count()==1:
	print("Iterative method is started.")
	for i in  REC_ISLICE:
		thi = Thread(target=IterateRec, args=[i])
		thi.start()

