import os

DIR_RAW_PROJ = "D:\\prjct\\Mausu\\Raw_Proj"    # specify path to directory with ordered raw object's Projections
DIR_FLAT = "D:\\prjct\\Mausu\\Flat"            # specify path to raw Flat image files (leave "" to ignore it)
DIR_DARK = "D:\\prjct\\Mausu\\Dark"            # specify path to raw Dark image files (leave "" to ignore it)

SCAN_ANGLE = 180           # enter the angle (degrees) at which the last projection was taken
PROJ_RESOL = (2048, 2048)  # enter resolution at which projection .dat files was written
PROJ_NUM = 1439            # projection quantity

MAKE_ISIN = [805]     # set a list with numbers of Sinograms to recover
REC_ISLICE = [800]    # set a list with numbers of Slices to recover

# run successively MakeSin.py and RecSlice.py scripts


DIR_PROJ = os.getcwd()+"\\Projections"
DIR_SIN = os.getcwd()+"\\Sinograms"
DIR_SLICE = os.getcwd()+"\\Slices"

# TILL IN TEST #
USE_CALIBR_AXIS = False       # find deviation of the axis of rotation before raw projection division
USE_CALIBR_ITERATE = True    # set True for applying iterative improving method after recovering slices
SHIFT = 200               	  # max shift range to find place of axis in; resolution of slice images will be decrised on SHIFT pixels
K = 0.6                       # the coefficient of correction of projections for the difference with the reconstructed projections when using the iterative method
