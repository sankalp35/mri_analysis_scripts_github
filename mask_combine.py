# Finds all the masks and then combines them into a single file
import subprocess
from fsl.wrappers.avwutils import fslmerge
from fsl.wrappers import fslreorient2std
import os
import shutil
from glob2 import glob
import fsl.utils.assertions as asrt
import time


dataDir = '/vols/Scratch/bnc208/friend_request_task'
print("This is the data directory: " + dataDir)

stage1Folder = '/d6_stage1_fslanat.feat'
mask_output_name = 'cmbmask_d6_fslanat'

subj_number = [2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24,26,27,28,29,30]

subj_mask_names = [];

for subj in subj_number:
    # Disable assertions
    asrt._DISABLE_ASSERTIONS = 1

    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)
    subjStage1 = subjPath + stage1Folder
    print("Starting with: " + subjPath)

    subjMask = subjStage1+'/reg_standard/mask.nii.gz'

    os.chdir(dataDir)


    if os.path.exists(dataDir+'/'+mask_output_name+'.nii.gz'):
        fslmerge('t', mask_output_name, mask_output_name, subjMask)
    else:
        shutil.copyfile(subjMask, mask_output_name+'.nii.gz')

    subj_mask_names.append(subjMask)


print(subj_mask_names)




