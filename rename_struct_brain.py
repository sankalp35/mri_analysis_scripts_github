#Preprocessing requires the struct_brain to have a corresponding struct
#This file will take a struct_brain_B (for eg) and then turn it into
#struct_B_brain and take the original struct and rename it struct_B
#this will preserve the sanity of the previous preprocessing file (they don't need to be modified)

#please change the respective directory where the change must happen before use

import os
import shutil
from python_script_utils import get_subj_numbers

dataDir = '/vols/Scratch/bnc208/friend_request_task'

struct_brain = 'synthstrip_biascorr_brain'
struct_brain_newname = 'synthstrip_biascorr_brain'

struct = 'T1_biascorr'
struct_newname = 'synthstrip_biascorr'

folder_containing_structs = '/preprocessPy/struct_brain.anat/'

subj_number = get_subj_numbers()


for subj in subj_number:
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    preprocessPath = subjPath + '/preprocessPy'
    folder_path = subjPath + folder_containing_structs

    print('Starting with'+folder_path)

    os.chdir(folder_path)

    if not os.path.exists(struct_newname):
        shutil.copyfile(struct + '.nii.gz', struct_newname+'.nii.gz')

    if not os.path.exists(struct_brain_newname+'.nii.gz'):
       shutil.copyfile(struct_brain+'.nii.gz', struct_brain_newname+'.nii.gz')

    if not os.path.exists(struct_brain_newname+'_mask'+'.nii.gz'):
       shutil.copyfile(struct_brain+'_mask'+'.nii.gz', struct_brain_newname+'_mask'+'.nii.gz')

    os.chdir(dataDir)



