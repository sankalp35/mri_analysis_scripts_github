import os
import shutil
from pathlib2 import Path
from fsl.wrappers import fslreorient2std, bet
from glob2 import glob
import os

dataDir = '/vols/Scratch/bnc208/friend_request_task/'

print("This is the data directory: " + dataDir)

os.chdir(dataDir)

# Subject names
subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
subj_number = int(subjInput)

# if the input is -1, then compute on all subjects
if subj_number == 99:
    subj_number = range(1, 31)
elif subj_number == 91:
    subjInputR = input("Start from which subject?: ")  # camel R stands for range
    subj_number = range(int(subjInputR), 31)
    print("Working on: " + str(subj_number))
else:
    subj_number = [int(subjInput)]

for subj in subj_number:
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    preprocessPath = subjPath + '/preprocessPy'

    # Expanded func = Full brain MRI (needs to be betted)
    expanded_func = glob(subjPath + '/raw/*011*bold*_WB*nii')[0]
    print("expanded func: " + expanded_func)

    # Alternate = high contrast (this will be used as example_func)
    if subj == 24:
        alternate_ref = glob(subjPath + '/raw/images_013*nii*')[0]
    else:
        alternate_ref = glob(subjPath + '/raw/images_012*nii*')[0]

    # reorient to std
    tostd_expfunc = fslreorient2std(expanded_func, preprocessPath + '/expanded_func.nii.gz', submit=True)
    tostd_altref = fslreorient2std(alternate_ref, preprocessPath + '/alternate_ref.nii.gz')

    # Navigate to local dir
    os.chdir(preprocessPath)

    # run Bet
    print("Starting BET.")
    bet_expfunc = bet('expanded_func', 'expanded_func_brain', m=True, f=0.05,
                      submit={'queue': 'veryshort.q', 'jobhold': tostd_expfunc})
    bet_altref = bet('alternate_ref', 'alternate_ref_brain', m=True, f=0.05,
                     submit={'queue': 'veryshort.q', 'jobhold': tostd_altref})

    print("Jobs in cluster")
