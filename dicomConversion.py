import os
from glob2 import glob

dataDir = '/vols/Scratch/bnc208/friend_request_task/'

os.chdir(dataDir)

#Subject names
subjInput = input("Enter subject number: ");
subj_number = [int(subjInput)];

for subj in subj_number:
    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)  # S01, S02, etc.

    rawFilePath = subjPath + '/raw'

    dicom = glob(subjPath+'/raw/*_TE18.4_13_*')[0]

    os.system('fsl_sub -q veryshort.q ' + 'dicom2nifti ' + dicom + ' ' + rawFilePath)

