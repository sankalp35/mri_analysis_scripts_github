#Transform mask to subject space and then extract time series for PPI analysis.

import os
import shutil
import csv
from pathlib2 import Path
from glob2 import glob
from fsl.wrappers import applywarp, flirt
from fsl.wrappers.wrapperutils import fslwrapper, applyArgStyle

#Custom fslmeants function (since it is not part of fslpy yet!)
@fslwrapper
def fslmeants(input, output, mask, **kwargs):
    cmd  = ['fslmeants', '-i', input, '-m', mask, '-o', output]
    return cmd + applyArgStyle('-=', **kwargs)

#Start
dataDir = '/vols/Scratch/bnc208/friend_request_task'



ppi_ts_path = dataDir+'/ppi-ts'

# Check whether the mask directory exists and if not create it
if not os.path.exists(ppi_ts_path):
    os.makedirs(ppi_ts_path)

included_masks = []

#Define masks and the copes they take
drn_mask_hailey = {
    'name': 'drn_mask_hailey',
    'path': dataDir+'/masks/drn_mask_hailey',
    'copes_of_interest': [2,3,9,10,11,12],
    'resolution': '2mm'
}

drn_mask_hailey_cropped = {
    'name': 'drn_mask_hailey_cropped',
    'path': dataDir+'/masks/drn_mask_hailey_cropped',
    'copes_of_interest': [2,3,9,10,11,12],
    'resolution': '2mm'
}

hypothalamus_mask_daria = {
    'name': 'hypothalamus_mask_daria',
    'path': dataDir+'/masks/hypothalamus_mask_daria',
    'copes_of_interest': [2,3,9,10,11,12],
    'resolution': '2mm'
}

anterior_insula_mask_hailey = {
    'name': 'anterior_insula_mask_hailey',
    'path': dataDir+'/masks/anterior_insula_mask_hailey',
    'copes_of_interest': [2,3,9,10,11,12],
    'resolution': '1mm'
}

drn_fa_mask = {
    'name': 'drn_fa_mask_1mm',
    'path': dataDir + '/masks/drn_fa_mask_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

hb_mask_miriam = {
    'name': 'hb_mask_miriam_1mm',
    'path': dataDir + '/masks/Hb_mask_miriam_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

sn_mask_hailey = {
    'name': 'sn_mask_hailey_1mm',
    'path': dataDir + '/masks/sn_mask_hailey_1mm',
    'copes_of_interest': [1,2,3,4,5,6,7,8,9],
    'resolution': '1mm'
}

feat_folder = 'd6_stage1.feat'


all_masks = [drn_mask_hailey, drn_mask_hailey_cropped, hypothalamus_mask_daria, anterior_insula_mask_hailey, drn_fa_mask]

for mask in all_masks:
    thisMaskInput = input("Work on "+ mask['name'] +" (Y=1/N=0): ")
    if int(thisMaskInput) == 1:
        included_masks.append(mask)


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
    subjName = '/S'+str(subj).zfill(2)
    subjName_txt = 'S'+str(subj).zfill(2)
    subjPath = dataDir+subjName


    #change directory to subj directory
    os.chdir(subjPath)
    
    #Transformation matrix path
    std2funcMat = feat_folder+'/reg/standard2example_func.mat'

    #ref
    ref = feat_folder+'/reg/example_func.nii.gz'

    #filtered func path
    filtered_func_path = feat_folder+'/filtered_func_data.nii.gz'

    #Check whether the mask directory exists and if not create it
    if not os.path.exists('masks'):
        os.makedirs('masks')

    if not os.path.exists('ppi_ts'):
        os.makedirs('ppi_ts')


    for this_mask in included_masks:
        subj_space_mask_path = 'masks/'+this_mask['name']+'_subjFuncspace.nii.gz'

        #applywarp to the mask to get to subject space
        appWarp_jid = applywarp(src=this_mask['path'], ref=ref, out=subj_space_mask_path, premat=std2funcMat, submit={'queue': 'short.q'})

        ts_output_path = 'ppi_ts' + '/' + this_mask['name'] + '_' + subjName_txt + '_' + '.txt'

        #extract time series from filtered_func
        fslmeants(input=filtered_func_path, mask=subj_space_mask_path, output=ts_output_path,
                  submit={'queue': 'veryshort.q', 'jobhold': appWarp_jid})
