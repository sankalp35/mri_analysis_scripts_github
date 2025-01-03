import os
import shutil
from pathlib2 import Path
from fsl.data.image import Image
from fsl.data.featanalysis import loadFsf
from glob2 import glob
import time

dataDir = '/vols/Scratch/bnc208/friend_request_task'

#Grab a template
drn_mask = 'drn_mask_hailey'
sn_mask = 'sn_mask_hailey'
vta_mask = 'vta_mask_hailey'

#designName
preprocessFeat = 'preprocessed_data.feat'
lowerLevelFeat = 'stage1ModDen.feat'

#Subject names
subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
subj_number = int(subjInput)

#if the input is 99, then compute on all subjects
if subj_number == 99:
    subj_number=range(1, 31)
elif subj_number == 91:
    subjInputR = input("Start from which subject?: ") #camel R stands for range
    subj_number = range(int(subjInputR), 31)
    print("Working on: " + str(subj_number))
else:
    subj_number = [int(subjInput)]

for subj in subj_number:
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    os.chdir(subjPath)

    os.system('fsl_sub -q short.q fslmeants -i preprocessed_data.feat/filtered_func_data -o ../ROIs/drnTimeSeries.txt -m ' + drn_mask)
    os.system('fsl_sub fslmeants -i preprocessed_data.feat/filtered_func_data -o ../ROIs/drnTimeSeries.txt -m ' + drn_mask)