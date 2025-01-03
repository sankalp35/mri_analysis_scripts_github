import os
import shutil
import csv
from pathlib2 import Path
from glob2 import glob
from fsl.wrappers import applywarp, flirt
from fsl.wrappers.wrapperutils import fslwrapper, applyArgStyle
from python_script_utils import get_subj_numbers


# Custom fslmeants function (since it is not part of fslpy yet!)
@fslwrapper
def fslmeants(input, output, mask, **kwargs):
    cmd = ['fslmeants', '-i', input, '-m', mask, '-o', output]
    return cmd + applyArgStyle('-=', **kwargs)

# Start
dataDir = '/vols/Scratch/bnc208/friend_request_task'

first_level_folder = 'd8_noITI_ppi_stage1_fslanat.feat'
    #'d6_stage1_fslanat.feat'

design_name = 'd8_noITI_ppi_stage1_fslanat'

included_masks = []

relevant_pes = [1,2,3,4,5,6]
                #2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] #d6

# Define masks and the pes they take
drn_mask_hailey = {
    'name': 'drn_mask_hailey_1mm',
    'path': dataDir + '/masks/drn_mask_hailey_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

drn_biased_mask = {
    'name': 'drn_biased_mask_1mm',
    'path': dataDir + '/masks/drn_biased_mask_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

drn_biased_anterior = {
    'name': 'drn_biased_anterior_1mm',
    'path': dataDir + '/masks/drn_biased_anterior_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

hypothalamus_mask_daria = {
    'name': 'hypothalamus_mask_daria_1mm',
    'path': dataDir + '/masks/hypothalamus_mask_daria_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

anterior_insula_mask_hailey = {
    'name': 'anterior_insula_mask_hailey_1mm',
    'path': dataDir + '/masks/anterior_insula_mask_hailey_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

sn_mask_hailey = {
    'name': 'sn_mask_hailey_1mm',
    'path': dataDir + '/masks/sn_mask_hailey_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

vta_mask_hailey = {
    'name': 'vta_mask_hailey_1mm',
    'path': dataDir + '/masks/vta_mask_hailey_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

sgACC_mask_sankalp = {
    'name': 'sgACC_mask_sankalp_1mm',
    'path': dataDir + '/masks/sgACC_biased_sankalp_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

area9_mask_marco = {
    'name': 'area9_mask_marco_1mm',
    'path': dataDir + '/masks/area9_mask_marco_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

hb_mask_miriam = {
    'name': 'hb_mask_miriam_1mm',
    'path': dataDir + '/masks/Hb_mask_miriam_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

drn_fa_mask = {
    'name': 'drn_fa_mask_1mm',
    'path': dataDir + '/masks/drn_fa_mask_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

L_anterior_insula_mask_hailey = {
    'name': 'L_anterior_insula_mask_hailey_1mm',
    'path': dataDir + '/masks/L_anterior_insula_mask_hailey_1mm',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

R_ins_func_mask = {
    'name': 'R_ins_func_mask',
    'path': dataDir + '/masks/R_ins_func_mask',
    'pes_of_interest': relevant_pes,
    'resolution': '1mm'
}

all_masks = [hypothalamus_mask_daria, anterior_insula_mask_hailey, sn_mask_hailey, vta_mask_hailey, area9_mask_marco, hb_mask_miriam, drn_fa_mask, L_anterior_insula_mask_hailey, R_ins_func_mask]

for mask in all_masks:
    thisMaskInput = input("Work on " + mask['name'] + " (Y=1/N=0): ")
    if int(thisMaskInput) == 1:
        included_masks.append(mask)

# Subject names
subj_number = get_subj_numbers()

for subj in subj_number:
    subjName = '/S' + str(subj).zfill(2)
    subjName_txt = 'S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    # change directory to subj directory
    os.chdir(subjPath)

    standard_pe_folder = 'standard_pe'
    if not os.path.exists(standard_pe_folder):
        os.makedirs(standard_pe_folder)

    for this_mask in included_masks:
        # Create a new ROI directory for this mask, if it does not exist already
        mask_ts_dir = '../roi-ts-pe/' + this_mask['name']
        if not os.path.exists(mask_ts_dir):
            os.makedirs(mask_ts_dir)
            print("Mask directory created inside ROI-TS")


        for this_pe in this_mask['pes_of_interest']:
            this_pe_path = first_level_folder + '/stats/pe' + str(this_pe) + '.nii.gz'

            # Formatting the pe name so it's easy to write
            pe_name = 'pe' + str(this_pe).zfill(2)
            registered_pe_path = standard_pe_folder + '/' + design_name + '_stdspace_' + pe_name

            if not os.path.exists(registered_pe_path + '.nii.gz'):  # Check if the file already exists

                exampleFunc2highres = first_level_folder + '/reg/example_func2highres.mat'
                warp = first_level_folder + '/reg/highres2standard_warp.nii.gz'

                ref = first_level_folder + '/reg/standard.nii.gz'

                appWarppe = applywarp(src=this_pe_path, ref=ref, out=registered_pe_path,
                                        premat=exampleFunc2highres,
                                        warp=warp, submit={'queue': 'short.q'})
                print("New standard PE in the oven")
            else:
                print(f"The file {registered_pe_path + '.nii.gz'} already exists, skipping the applywarp stage.")

            design_folder_ts = mask_ts_dir + '/' + design_name

            # Check if directory exists
            if not os.path.exists(design_folder_ts):
                # If not, then create it
                os.makedirs(design_folder_ts)
                print("Created output folder for this design")

            ts_output_path = design_folder_ts + '/' + this_mask['name'] + '_' + subjName_txt + '_' + pe_name + '.txt'

            if not os.path.exists(registered_pe_path + '.nii.gz'):
                # Extract time series using custom defined fslmeants function
                fslmeants(input=registered_pe_path, mask=this_mask['path'], output=ts_output_path,
                              submit={'queue': 'short.q', 'jobhold': appWarppe})
            else:
                fslmeants(input=registered_pe_path, mask=this_mask['path'], output=ts_output_path,
                          submit={'queue': 'short.q'}) #run without job hold

