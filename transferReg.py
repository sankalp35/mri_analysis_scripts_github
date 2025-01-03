#This script transfers


import os
import shutil
from pathlib2 import Path
from fsl.data.image import Image
from fsl.data.featanalysis import loadFsf
from glob2 import glob
import time

dataDir = '/vols/Scratch/bnc208/friend_request_task'

#designName
preprocessFeat = 'preprocessed_data_fslAnat_synthstrip_altref_intensityNormalisedStructAndFuncExpFunc_fullsearch.feat'

#folder to transfer to
lowerLevelFeat = 'd8_noITI_ppi_stage1_fslanat.feat'


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

    #src and dest paths
    reg_path = subjPath+'/'+preprocessFeat+"/reg"
    dest = subjPath+'/'+lowerLevelFeat

    if os.path.exists(reg_path) & os.path.exists(dest):
        os.system('fsl_sub -q veryshort.q cp -R '+reg_path+' '+dest)
        print("Copied "+subjName)
       # shutil.copytree(reg_path, dest, dirs_exist_ok=True)







