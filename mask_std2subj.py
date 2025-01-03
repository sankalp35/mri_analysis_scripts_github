#Takes masks and transforms them to functional space
#Then extracts time series from the functional image


import os
import shutil
import csv
from pathlib2 import Path
from glob2 import glob
from fsl.wrappers import applywarp, flirt
from fsl.wrappers.wrapperutils import fslwrapper, applyArgStyle
from python_script_utils import get_subj_numbers

#Custom fslmeants function (since it is not part of fslpy yet!)
@fslwrapper
def fslmeants(input, output, mask, **kwargs):
    cmd  = ['fslmeants', '-i', input, '-m', mask, '-o', output]
    return cmd + applyArgStyle('-=', **kwargs)

#Start
dataDir = '/vols/Scratch/bnc208/friend_request_task'


#data directory
dataDir = '/vols/Scratch/bnc208/friend_request_task'

first_level_folder = 'd6_stage1_fslanat.feat'

design_name = 'd6_fslanatSynthstrip'


included_masks = []


# Define masks and the funcs they take
drn_mask_hailey = {
    'name': 'drn_mask_hailey_1mm',
    'path': dataDir + '/masks/drn_mask_hailey_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

drn_biased_mask = {
    'name': 'drn_biased_mask_1mm',
    'path': dataDir + '/masks/drn_biased_mask_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

drn_biased_anterior = {
    'name': 'drn_biased_anterior_1mm',
    'path': dataDir + '/masks/drn_biased_anterior_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

hypothalamus_mask_daria = {
    'name': 'hypothalamus_mask_daria_1mm',
    'path': dataDir + '/masks/hypothalamus_mask_daria_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

anterior_insula_mask_hailey = {
    'name': 'anterior_insula_mask_hailey_1mm',
    'path': dataDir + '/masks/anterior_insula_mask_hailey_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

sn_mask_hailey = {
    'name': 'sn_mask_hailey_1mm',
    'path': dataDir + '/masks/sn_mask_hailey_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

vta_mask_hailey = {
    'name': 'vta_mask_hailey_1mm',
    'path': dataDir + '/masks/vta_mask_hailey_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

sgACC_mask_sankalp = {
    'name': 'sgACC_mask_sankalp_1mm',
    'path': dataDir + '/masks/sgACC_biased_sankalp_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

area9_mask_marco = {
    'name': 'area9_mask_marco_1mm',
    'path': dataDir + '/masks/area9_mask_marco_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

hb_mask_miriam = {
    'name': 'hb_mask_miriam_1mm',
    'path': dataDir + '/masks/Hb_mask_miriam_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

drn_fa_mask = {
    'name': 'drn_fa_mask_1mm',
    'path': dataDir + '/masks/drn_fa_mask_1mm',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

lc_mask_miriam = {
    'name': 'lc_mask_miriam_1mm',
    'path': dataDir + '/masks/AAN_LC_1mm_miriam.nii',
    'funcs_of_interest': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    'resolution': '1mm'
}

all_masks = [drn_mask_hailey, drn_biased_mask, drn_biased_anterior, hypothalamus_mask_daria, anterior_insula_mask_hailey, sn_mask_hailey, vta_mask_hailey, sgACC_mask_sankalp, area9_mask_marco, hb_mask_miriam, drn_fa_mask, lc_mask_miriam]


for mask in all_masks:
    thisMaskInput = input("Work on "+ mask['name'] +" (Y=1/N=0): ")
    if int(thisMaskInput) == 1:
        included_masks.append(mask)


#Subject names
subj_number = get_subj_numbers()

for subj in subj_number:
    subjName = '/S'+str(subj).zfill(2)
    subjName_txt = 'S'+str(subj).zfill(2)
    subjPath = dataDir+subjName

    #change directory to subj directory
    os.chdir(subjPath)


    #Transformation matrix path
    std2funcMat = first_level_folder+'/reg/standard2example_func.mat'

    #ref
    ref = first_level_folder+'/reg/example_func.nii.gz'

    #Check whether the mask directory exists and if not create it
    if not os.path.exists('masks_subjSpace'):
        os.makedirs('masks_subjSpace')

    for this_mask in included_masks:
        subj_space_mask_path = 'masks/'+this_mask['name']+design_name+'_subjspace.nii.gz'

        if not os.path.exists(subj_space_mask_path):
            # applywarp to the mask to get to subject space
            appWarp_jid = applywarp(src=this_mask['path'], ref=ref, out=subj_space_mask_path, premat=std2funcMat,
                                    submit={'queue': 'short.q'})
            print("Transforming mask to subject space")
        else:
            print("Mask exists in subject space, not applying warp")

        #Create a new ROI directory if it does not exist already
        if not os.path.exists('../roi-tc-func'):
            os.makedirs('../roi-tc-func')

        #Create a new ROI directory for this mask, if it does not exist already
        mask_ts_dir = '../roi-tc-func/'+this_mask['name']
        if not os.path.exists(mask_ts_dir):
            os.makedirs(mask_ts_dir)

        this_func_path = first_level_folder+'/filtered_func_data.nii.gz'

        ts_output_path = mask_ts_dir+'/'+this_mask['name']+'_'+subjName_txt+'.txt'

        #Extract time series using custom defined fslmeants function
        fslmeants(input=this_func_path, mask=subj_space_mask_path, output=ts_output_path,
                submit={'queue': 'veryshort.q', 'jobhold': appWarp_jid})




