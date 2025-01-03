import os
import shutil
import csv
from pathlib2 import Path
from glob2 import glob
from fsl.wrappers import applywarp, flirt
from fsl.wrappers.wrapperutils import fslwrapper, applyArgStyle


# Custom fslmeants function (since it is not part of fslpy yet!)
@fslwrapper
def fslmeants(input, output, mask, **kwargs):
    cmd = ['fslmeants', '-i', input, '-m', mask, '-o', output]
    return cmd + applyArgStyle('-=', **kwargs)


# Start
dataDir = '/vols/Scratch/bnc208/friend_request_task'

first_level_folder = 'd6_stage1.feat'

design_name = 'd6'

included_masks = []


# Define masks and the copes they take
drn_mask_hailey = {
    'name': 'drn_mask_hailey_1mm',
    'path': dataDir + '/masks/drn_mask_hailey_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

drn_biased_mask = {
    'name': 'drn_biased_mask_1mm',
    'path': dataDir + '/masks/drn_biased_mask_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

drn_biased_anterior = {
    'name': 'drn_biased_anterior_1mm',
    'path': dataDir + '/masks/drn_biased_anterior_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

hypothalamus_mask_daria = {
    'name': 'hypothalamus_mask_daria_1mm',
    'path': dataDir + '/masks/hypothalamus_mask_daria_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

anterior_insula_mask_hailey = {
    'name': 'anterior_insula_mask_hailey_1mm',
    'path': dataDir + '/masks/anterior_insula_mask_hailey_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

sn_mask_hailey = {
    'name': 'sn_mask_hailey_1mm',
    'path': dataDir + '/masks/sn_mask_hailey_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

vta_mask_hailey = {
    'name': 'vta_mask_hailey_1mm',
    'path': dataDir + '/masks/vta_mask_hailey_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

sgACC_mask_sankalp = {
    'name': 'sgACC_mask_sankalp_1mm',
    'path': dataDir + '/masks/sgACC_biased_sankalp_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

area9_mask_marco = {
    'name': 'area9_mask_marco_1mm',
    'path': dataDir + '/masks/area9_mask_marco_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

hb_mask_miriam = {
    'name': 'hb_mask_miriam_1mm',
    'path': dataDir + '/masks/Hb_mask_miriam_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

drn_fa_mask = {
    'name': 'drn_fa_mask_1mm',
    'path': dataDir + '/masks/drn_fa_mask_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

all_masks = [drn_mask_hailey, drn_biased_mask, drn_biased_anterior, hypothalamus_mask_daria, anterior_insula_mask_hailey, sn_mask_hailey, vta_mask_hailey, sgACC_mask_sankalp, area9_mask_marco, hb_mask_miriam, drn_fa_mask]

for mask in all_masks:
    thisMaskInput = input("Work on " + mask['name'] + " (Y=1/N=0): ")
    if int(thisMaskInput) == 1:
        included_masks.append(mask)

# Subject names
subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
subj_number = int(subjInput)

# if the input is 99, then compute on all subjects
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
    subjName_txt = 'S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    # change directory to subj directory
    os.chdir(subjPath)

    standard_cope_folder = 'standard_cope'
    if not os.path.exists(standard_cope_folder):
        os.makedirs(standard_cope_folder)

    for this_mask in included_masks:
        # Create a new ROI directory for this mask, if it does not exist already
        mask_ts_dir = '../roi-ts/' + this_mask['name']
        if not os.path.exists(mask_ts_dir):
            os.makedirs(mask_ts_dir)


        for this_cope in this_mask['copes_of_interest']:
            this_cope_path = first_level_folder + '/stats/cope' + str(this_cope) + '.nii.gz'

            # Formatting the cope name so it's easy to write
            cope_name = 'cope' + str(this_cope).zfill(2)
            registered_cope_path = standard_cope_folder + '/' + design_name + '_stdspace_' + cope_name

            if not os.path.exists(registered_cope_path + '.nii.gz'):  # Check if the file already exists

                exampleFunc2highres = first_level_folder + '/reg/example_func2highres.mat'
                warp = first_level_folder + '/reg/highres2standard_warp.nii.gz'

                ref = first_level_folder + '/reg/standard.nii.gz'

                appWarpCope = applywarp(src=this_cope_path, ref=ref, out=registered_cope_path,
                                        premat=exampleFunc2highres,
                                        warp=warp, submit={'queue': 'short.q'})
            else:
                print(f"The file {registered_cope_path + '.nii.gz'} already exists, skipping the applywarp stage.")

            design_folder_ts = mask_ts_dir + '/' + design_name

            # Check if directory exists
            if not os.path.exists(design_folder_ts):
                # If not, then create it
                os.makedirs(design_folder_ts)
                print("Created output folder for this design")

            ts_output_path = design_folder_ts + '/' + this_mask['name'] + '_' + subjName_txt + '_' + cope_name + '.txt'

            if not os.path.exists(registered_cope_path + '.nii.gz'):
                # Extract time series using custom defined fslmeants function
                fslmeants(input=registered_cope_path, mask=this_mask['path'], output=ts_output_path,
                          submit={'queue': 'veryshort.q', 'jobhold': appWarpCope})
            else:
                fslmeants(input=registered_cope_path, mask=this_mask['path'], output=ts_output_path,
                          submit={'queue': 'veryshort.q'}) #run without job hold

