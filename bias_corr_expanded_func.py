from biascorrect import bias_correct_fslmath, bias_correction_fsl
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

    input_func = preprocessPath + '/expanded_func_brain.nii.gz'
    output_func = preprocessPath + '/bias_corr_expanded_func_brain.nii.gz'
    bias_field = preprocessPath+'/bias_corr_expanded_func_brain_bias.nii.gz'
    output = preprocessPath + '/expanded_func_brain_bias.nii.gz'

    if operation == 1:
        bias_correction_fsl(input_func, output_func)
    else:
        bias_correct_fslmath(input_func, bias_field, output)

