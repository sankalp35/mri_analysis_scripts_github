#Bet with intensity normalising

from fsl.wrappers import fslreorient2std, bet, fslmaths, fsl_prepare_fieldmap, fsl_sub
from fsl.utils.run import hold
import os
from glob2 import glob
dataDir = '/vols/Scratch/bnc208/friend_request_task/'

print("This is the data directory: " +dataDir)

os.chdir(dataDir)


#Subject names
subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
subj_number = int(subjInput)

#if the input is -1, then compute on all subjects
if subj_number == 99:
    subj_number=range(1, 31)
elif subj_number == 91:
    subjInputR = input("Start from which subject?: ") #camel R stands for range
    subj_number = range(int(subjInputR), 31)
    print("Working on: " + str(subj_number))
else:
    subj_number = [int(subjInput)]

for subj in subj_number:
    subjName = '/S'+str(subj).zfill(2)
    subjPath = dataDir+subjName

    preprocessPath = subjPath + '/preprocessPy'

    os.chdir(preprocessPath)

    if os.path.exists('struct_brain_B_f0.12.nii.gz'):
        os.remove('struct_brain_B_f0.12.nii.gz')
        print("old bet file deleted")

    bet('struct', 'struct_brain_B_f0.12', m=True, f=0.12, B=True, submit=True)
