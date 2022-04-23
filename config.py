import os

DIR_RAW_PROJ = "D:\\prjct\\Mausu\\Raw_Proj"    # specify path to directory with ordered raw object's Projections
DIR_FLAT = "D:\\prjct\\Mausu\\Flat"            # specify path to raw Flat image file (leave "" to ignore it)
DIR_DARK = "D:\\prjct\\Mausu\\Dark"            # specify path to raw Dark image file (leave "" to ignore it)

SCAN_ANGLE = 180           # enter the angle (degrees) at which the last projection was taken
PROJ_RESOL = (2048, 2048)  # enter resolution at which projection .dat files was written

MAKE_ISIN = [815, 820]     # set a list with numbers of Sinograms to recover
REC_ISLICE = [815, 820]    # set a list with numbers of Slices to recover

STEP = 1                   # for making sinograms with skipping projections with the step equals STEP

# run successively MakeSin.py and RecSlice.py scripts


DIR_PROJ = os.getcwd()+"\\Projections2"
DIR_SIN = os.getcwd()+"\\Sinograms"
DIR_SLICE = os.getcwd()+"\\Slices"

USE_CALIBR = True         # only for SCAN_ANGLE = 180!
SHIFT = 200               # resolution of slice image will be decrised on SHIFT pixels
K = 0.1
