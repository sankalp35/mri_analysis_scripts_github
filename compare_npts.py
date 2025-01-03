#Compare npts for raw and preprocessed MRI files to determine if they are the same size


import os
from glob2 import glob
from fsl.data.image import Image

dataDir = '/vols/Scratch/bnc208/friend_request_task'


print("This is the data directory: " +dataDir)

os.chdir(dataDir)

#Output folder, input 4d, etc. is set up through the template.

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
    #subject path
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName + '/'


    #get raw file
    func_raw = Image(glob(subjPath + '/raw/13_*')[0])

    #get preprocesssed file
    func_preprocess = Image(glob(subjPath + '/preprocessPy/func.nii.gz')[0])

    raw_npts = func_raw.header.get("dim")[4]
    preproc_npts = func_preprocess.header.get("dim")[4]

    if raw_npts == preproc_npts:
        print("Subject " + str(subj) + " npts matched " +str(raw_npts) + " x " + str(preproc_npts))
    else:
        print("NPTS DID NOT MATCH, subject: " + str(subj) + " " +str(raw_npts) + " x " + str(preproc_npts))


