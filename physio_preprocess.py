import os
from glob2 import glob

dataDir = '/vols/Scratch/bnc208/friend_request_task/'

print("This is the data directory: " +dataDir)

os.chdir(dataDir)

#in range function 30 is not included. Subject 30 needs to be dealt with separately because their .txt was not retrieved.
#So I converted the acq file using acq2txt using a python package.
for subj in range(1,2):
    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)  # S01, S02, etc.
    preprocessPath = subjPath + '/preprocessPy'

    print("Starting with: " + subjPath)
    os.chdir(subjPath + '/behavioural')

    #get the input values for PNM
    func = preprocessPath + '/func.nii.gz'
    biopac = glob('*biopac*.txt')[0]
    slice_timings = glob(dataDir + '*slice_timing_file*')[0]

    print(biopac)
    print(slice_timings)


    os.system('/opt/fmrib/fsl/bin/fslFixText ' + biopac + ' ' + subjPath + '/behavioural/pnmPy_input.txt')

    while not os.path.exists(subjPath + '/behavioural/pnmPy_input.txt'):
     time.sleep(10)
     print("sleeping - waiting for fslFixText")

    print("Starting stage 1")
    os.system('/opt/fmrib/fsl/bin/pnm_stage1 -i pnmPy_input.txt -o pnmPy -s 200 --tr = 2.03 --smoothcard=0.1 --smoothresp=0.1 --resp=1 --cardiac=2 --trigger=3 --rvt')

    print("Check output in the browser")

os.chdir(dataDir)

