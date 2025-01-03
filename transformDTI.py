# Take FA map and transforms it into subject space

from fsl.wrappers import fslreorient2std, bet
from fsl.wrappers.flirt import flirt
from fsl.wrappers.fnirt import applywarp
import subprocess
from fsl.wrappers.avwutils import _fslmerge
import os
from glob2 import glob
import fsl.utils.assertions as asrt
import time


dataDir = '/vols/Scratch/bnc208/friend_request_task'
print("This is the data directory: " + dataDir)

#Subject names
subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
subj_number = int(subjInput)

#if the input is 99, then compute on all subjects
if subj_number == 99:
    subj_number = range(1, 31)
elif subj_number == 91:
    subjInputR = input("Start from which subject?: ") #camel R stands for range
    subj_number = range(int(subjInputR), 31)
    print("Working on: " + str(subj_number))
else:
    subj_number = [int(subjInput)]


for subj in subj_number:
    asrt._DISABLE_ASSERTIONS = 1

    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)

    os.chdir(subjPath)

    dti_fa_original = subjPath+"/preprocessPy/dti_FA.nii.gz"
    dti_fa_subjspace = subjPath+"/preprocessed_data.feat/dti_fa_subjspace.nii.gz"
    highres = subjPath+"/preprocessed_data.feat/reg/highres.nii.gz"


    reorient_jid = fslreorient2std(dti_fa_original, subjPath+"/preprocessPy/dti_FA_reoriented.nii.gz", submit={'queue': 'short.q'})
    applywarp(src=subjPath+"/preprocessPy/dti_FA_reoriented_brain.nii.gz", ref=highres, out=dti_fa_subjspace, submit={'queue': 'short.q'})



