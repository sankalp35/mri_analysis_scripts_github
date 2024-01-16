import shutil
from fsl.wrappers import fslreorient2std, fsl_anat, fslmaths, fsl_prepare_fieldmap, applywarp, flirt, applyxfm
import fsl_sub
from fsl.utils.run import hold
import os
from glob2 import glob
from python_script_utils import get_subj_numbers
import time

dataDir = '/vols/Scratch/bnc208/friend_request_task/'

print("This is the data directory: " + dataDir)

os.chdir(dataDir)

# Prompt for user input outside the loop
run_bet = input("Run basic brain extraction and bias correct (fsl_anat) for all subjects? (0 for no, 1 for yes): ")
run_synthstrip = input("Run advanced brain extraction (synthstrip) for all subjects? (0 for no, 1 for yes): ")
run_mask_struct2epi = input("Register mask to epi? (0 for no, 1 for yes): ")

subj_number = get_subj_numbers();

for subj in subj_number:
    subjPath = dataDir + '/S' + str(subj).zfill(2)  # S01, S02, etc.
    preprocessPath = subjPath + '/preprocessPy'

    doesExist = os.path.exists(preprocessPath)
    if not doesExist:
        os.makedirs(preprocessPath)
        print("The new preprocess is created!")

    print("Starting with: " + subjPath)

    structural = glob(subjPath + '/raw/*MPRAGE*nii*')[0]
    fmap_mag = glob(subjPath + '/raw/images_08*nii*')[0]
    fmap_phase = glob(subjPath + '/raw/images_09*nii*')[0]
    expanded_func = glob(subjPath + '/raw/images_012*nii*')[0]
    func = "func.nii.gz"

    # Reorient everything to standard (commented out)
    # fslreorient2std(structural, preprocessPath + '/struct.nii.gz')
    # fslreorient2std(func, preprocessPath + '/func.nii.gz', submit={'queue': 'veryshort.q'})
    # fslreorient2std(fmap_mag, preprocessPath + '/fmap_mag.nii.gz')
    # fslreorient2std(fmap_phase, preprocessPath + '/fmap_phase.nii.gz')
    # fslreorient2std(expanded_func, preprocessPath + '/expanded_func.nii.gz')

    os.chdir(preprocessPath)


    import subprocess

    t1 = 'struct_brain.anat/T1_biascorr.nii.gz'
    t1_brain = 'struct_brain.anat/synthstrip_biascorr_brain.nii.gz'
    brain_mask = "struct_brain.anat/synthstrip_biascorr_brain_mask.nii.gz"  # Replace with the actual mask file path


    if run_bet == "1":
        print("Starting BET.")

        if os.path.exists('struct_brain.anat'):
            shutil.rmtree('struct_brain.anat')
            print('Deleted pre-existing struct_brain.anat folder')

        struct_fslanat_jid = fsl_anat('struct', 'struct_brain', t="T1", betfparam=0.1, submit=True)
    else:
        print("Skipping brain extraction.")

    if run_synthstrip == "1":
        print("Starting synthstrip")
        if run_bet == "1":
            fsl_sub.submit(queue="short.q",
                    jobhold=struct_fslanat_jid,
                    command=['/vols/Scratch/flange/bin/synthstrip-singularity', "-i", t1, "-o", t1_brain, "-m", brain_mask, "--no-csf"])
        else:
            # Run synthstrip without the -j flag
            fsl_sub.submit(queue="short.q",
                           command=['/vols/Scratch/flange/bin/synthstrip-singularity', "-i", t1, "-o", t1_brain, "-m",
                                    brain_mask, "--no-csf"])
    else:
        print("Not running synthstrip")

    if run_mask_struct2epi == "1":
        print("Registering mask to EPI space")
        #first register structural to epi using flirt
        flirtJ = flirt(src=t1_brain, ref=func, omat="affine_structBrain2func.mat", out="structBrain2func.nii.gz", submit=True)
        applyxfm = applyxfm(src=brain_mask, ref=func, mat="affine_structBrain2func.mat", out="brainmask_struct2func.nii.gz", submit={'j': flirtJ})





    os.chdir(dataDir)

    # fmap_jid = bet('fmap_mag', 'fmap_mag_brain', submit={'queue': 'veryshort.q'})
    # bet('expanded_func', 'expanded_func_brain', f=0.05, submit={'queue': 'veryshort.q'})

    # hold([fmap_jid])
    # fmap_ero_jid = fslmaths('fmap_mag_brain').ero().run('fmap_mag_brain_ero')

    # print("Preparing fieldmap image")
    # fsl_prepare_fieldmap('fmap_phase.nii.gz', 'fmap_mag_brain_ero', 'fmap_rads', 1.02, submit={'
