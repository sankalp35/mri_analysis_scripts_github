#This file takes in biascorr py program and implements it for all subjects

from biascorrect import bias_correction_fsl, bias_correct_fslmath
import os
from python_script_utils import get_subj_numbers
import fsl.utils.assertions as asrt

dataDir = '/vols/Scratch/bnc208/friend_request_task'
print("This is the data directory: " + dataDir)

subj_number = get_subj_numbers()
operation = int(input("Press 1 to calculate bias field, 2 to apply it"))

for subj in subj_number:
    # Disable assertions
    asrt._DISABLE_ASSERTIONS = 1

    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)
    preprocessPath = subjPath + '/preprocessPy'
    print("Starting with: " + subjPath)

    os.chdir(subjPath)

    input_func = preprocessPath+'/func.nii.gz'
    output_func = preprocessPath+'/bias_corrected_func.nii.gz'

    if operation == 1:
        bias_correction_fsl(input_func,  output_func) #output_func serves as the output basename
    else:
        bias_correct_fslmath(input_func, preprocessPath+'/bias_corrected_func_bias.nii.gz', output_func) #functional, biasfield




