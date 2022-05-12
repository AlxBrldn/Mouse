import os
from config import *

import sys, os, math, random
from time import time
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
import skimage.io as io
from skimage.transform import iradon, rescale, radon
from skimage import io
from skimage.data import shepp_logan_phantom
#from scipy.optimize import minimize
#from scipy.optimize import fmin
from natsort import natsorted
import imageio
from PIL import Image
import PIL

def DivI():
	files = os.listdir(DIR_RAW_PROJ)
	files = natsorted(files)#[::-1]
	
	dfn = os.listdir(DIR_DARK)
	dfn = natsorted(dfn)
	
	ffn = os.listdir(DIR_FLAT)
	ffn = natsorted(ffn)#[::-1]

	with open(DIR_DARK+"\\"+dfn[0], "rb") as file:
		byte_content = file.read()
		dark = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
	dark = np.asarray(dark).reshape(PROJ_RESOL)
	with open(DIR_FLAT+"\\"+ffn[0], "rb") as file:
		byte_content = file.read()
		flate = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
	flate = np.asarray(flate).reshape(PROJ_RESOL)
		
	with open(DIR_RAW_PROJ+"\\"+files[0], "rb") as file:
		byte_content = file.read()
		proj = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
	
	proj = np.asarray(proj).reshape(PROJ_RESOL)
	proj = np.asarray(np.around(255*np.divide((proj-dark), (flate-dark))), dtype='uint8')
	imageio.imwrite(DIR_PROJ+"\\sp_0.bmp", proj)
	
	with open(DIR_DARK+"\\"+dfn[-1], "rb") as file:
		byte_content = file.read()
		dark = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
	dark = np.asarray(dark).reshape(PROJ_RESOL)
	with open(DIR_FLAT+"\\"+ffn[-1], "rb") as file:
		byte_content = file.read()
		flate = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
	flate = np.asarray(flate).reshape(PROJ_RESOL)
		
	with open(DIR_RAW_PROJ+"\\"+files[-1], "rb") as file:
		byte_content = file.read()
		proj = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
	
	proj = np.asarray(proj).reshape(PROJ_RESOL)
	proj = np.asarray(np.around(255*np.divide((proj-dark), (flate-dark))), dtype='uint8')
	imageio.imwrite(DIR_PROJ+"\\sp_1439.bmp", proj)

def United_Kingdoom(part, arr):
	if(part==0):
		return arr
	p=0
	#print(arr)
	while(p+part<arr.shape[0]):
		s = np.sum(arr[p:p+part,:], axis=0)/part
		#print(s)
		arr[p:p+part,:] = s
		#print(arr[p:p+part+1,:])
		p += part
	
	s = np.sum(arr[p:,:], axis=0)/(arr.shape[0]-p)
	arr[p:,:] = s
	#print("!!!!!!!!!!!")
	#print(arr)
	return arr
	

def hi2(pf, pl):
	pl = np.asarray(pl)
	pl = pl[:,:,0] + pl[:,:,1] + pl[:,:,2]
	pl = United_Kingdoom(UNITE, pl)
	return np.power((pf-pl)[:,SHIFT:-SHIFT], 2).sum(axis=1)
def Calibr_Axis():
	DivI()
	
	files = os.listdir(DIR_PROJ)
	files = natsorted(files)

		
	pf = Image.open(DIR_PROJ+"\\"+files[0])
	pl = Image.open(DIR_PROJ+"\\"+files[-1])
	pf = np.asarray(pf).reshape(PROJ_RESOL)
	pl = np.asarray(pl).reshape(PROJ_RESOL)
	pf = United_Kingdoom(UNITE, pf)
	#pl = United_Kingdoom(UNITE, pl)
	plt.imsave(os.getcwd()+"\\pf.bmp", np.asarray(pf, dtype='uint8'), cmap = plt.cm.gray)
	plt.imsave(os.getcwd()+"\\pl.bmp", np.asarray(pl,dtype='uint8'), cmap = plt.cm.gray)
		
	pf = Image.open(os.getcwd()+"\\pf.bmp")
	pf.show()
	pf = np.asarray(pf)
	pf = pf[:,:,0] + pf[:,:,1] + pf[:,:,2]
	#pf = United_Kingdoom(UNITE, pf)
	
	pl = Image.open(os.getcwd()+"\\pl.bmp").transpose(PIL.Image.FLIP_LEFT_RIGHT) #Image.open(DIR_PROJ+"\\pf.jpg").rotate(2, translate=(0,0))#Image.open(DIR_PROJ+"\\pl.jpg").transpose(PIL.Image.FLIP_LEFT_RIGHT)

	
	minhi2 = [1000000000000 for i in range(0, pf.shape[0])]
	min_shifts = [-1 for i in range(0, pf.shape[0])]
	for i in range(-SHIFT, SHIFT):
		plr = pl.rotate(0, translate=(i,0))
		hi = hi2(pf, plr)
		miner = [k for k, v in enumerate(minhi2) if v>hi[k]]
		for j in miner:
			min_shifts[j] = i
			minhi2[j] = hi[j]
	plt.plot([i for i in range(SHIFT, pf.shape[0]-SHIFT)], min_shifts[SHIFT:-SHIFT])
	plt.show()

def MakeSin(isin, DIR_PROJ):
	files = os.listdir(DIR_PROJ)
	files = natsorted(files)
	sinogram = list()
	for fn in files:
		p = np.array(Image.open(DIR_PROJ+"\\"+fn))[isin]
		#p = p[:,0] + p[:,1] + p[:,2]
		sinogram.append(p)
		print("Process file: ", fn, end="\r")
	plt.imsave(DIR_SIN+"\\s"+str(isin)+".bmp", np.asarray(sinogram, dtype='uint8'), cmap = plt.cm.gray)
	
def divideIminAll():    # For creation sinograms with dark and flat files
	files = os.listdir(DIR_RAW_PROJ)
	files = natsorted(files)#[::-1]
	
	dfn = os.listdir(DIR_DARK)
	dfn = natsorted(dfn)
	darkstep = round(len(files)/len(dfn))
	
	ffn = os.listdir(DIR_FLAT)
	ffn = natsorted(ffn)#[::-1]
	flatstep = round(len(files)/len(ffn))
	
	if DIR_FLAT=="":
		flate = np.zeros(PROJ_RESOL)
	if DIR_DARK=="":
		dark = np.zeros(PROJ_RESOL)
	
	i=0
	di=0
	fi=0
	for fn in files:
		if (i)%darkstep==0 or i==0 and i!=1 and DIR_DARK!="":
			with open(DIR_DARK+"\\"+dfn[di], "rb") as file:
				byte_content = file.read()
				dark = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
			dark = np.asarray(dark).reshape(PROJ_RESOL)
			di += 1
		if (i)%flatstep==0 or i==0 and i!=1 and DIR_FLAT!="":
			with open(DIR_FLAT+"\\"+ffn[fi], "rb") as file:
				byte_content = file.read()
				flate = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
			flate = np.asarray(flate).reshape(PROJ_RESOL)
			fi += 1
			
		with open(DIR_RAW_PROJ+"\\"+fn, "rb") as file:
			byte_content = file.read()
			proj = [byte_content[u + 1] << 8 | byte_content[u] for u in range(0, len(byte_content), 2)]
		
		proj = np.asarray(proj).reshape(PROJ_RESOL)
		proj = np.asarray(np.around(255*np.divide((proj-dark), (flate-dark))), dtype='uint8')
		imageio.imwrite(DIR_PROJ+"\\sp_"+str(i)+".bmp", proj)
		#plt.imsave(DIR_PROJ+"\\sp_"+str(i)+".bmp", proj, cmap = plt.cm.gray)
		print ("Complete: ", round(i*100/len(files), 1), "%", end="\r")
		i += 1

if os.path.isdir(DIR_PROJ+"\\")==False:
	print("Directory with proceed divided projections isn't found. It will be created at " + DIR_PROJ + ".")
	os.mkdir(DIR_PROJ)
	print("Starting projection processing...")
	print (" ", end="\r")
	divideIminAll()
if USE_CALIBR_AXIS==True:
	print("Axis calibration is started... ")
	Calibr_Axis()
	print("Done.")
if os.path.isdir(DIR_SIN+"\\")==False:
	print("Create directory with sinograms at " + DIR_SIN + ".")
	os.mkdir(DIR_SIN)
	print("Done.")
print("Creating sinograms...")
for i in MAKE_ISIN:
	th = Thread(target=MakeSin, args=(i, DIR_PROJ))
	th.start()
