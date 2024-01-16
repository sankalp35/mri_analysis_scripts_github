from fsl.wrappers import fslreorient2std, bet, fslmaths, fsl_prepare_fieldmap, fsl_sub
from fsl.utils.run import hold
import os
from glob2 import glob
import time

dataDir = '/vols/Scratch/bnc208/friend_request_task/'

print("This is the data directory: " +dataDir)

os.chdir(dataDir)

#Subject names
subjInput = input("Enter subject number: ");
subj_number = [int(subjInput)];

#Customise pipeline



for subj in subj_number:
    #Define where the subject specific raw files are stored
    subjPath = dataDir+'/S'+str(subj).zfill(2) #S01, S02, etc.
    preprocessPath = subjPath+'/preprocessPy'

    #create preprocess directory if does not exists
    # Check whether the specified path exists or not
    doesExist = os.path.exists(preprocessPath)
    if not doesExist:
        # Create a new directory because it does not exist
        os.makedirs(preprocessPath)
        print("The new preprocess is created!")

    print("Starting with: "+subjPath)

    #Get raw files
    structural = glob(subjPath+'/raw/*MPRAGE*nii*')[0]
    func = glob(subjPath+'/raw/13_*')[0]
    fmap_mag = glob(subjPath+'/raw/images_08*nii*')[0]
    fmap_phase = glob(subjPath+'/raw/images_09*nii*')[0]
    expanded_func = glob(subjPath+'/raw/images_012*nii*')[0]

    #Reorient everything to standard
    fslreorient2std(structural, preprocessPath+'/struct.nii.gz')
    fslreorient2std(func, preprocessPath+'/func.nii.gz', submit={'queue': 'veryshort.q'})
    fslreorient2std(fmap_mag, preprocessPath+'/fmap_mag.nii.gz')
    fslreorient2std(fmap_phase, preprocessPath+'/fmap_phase.nii.gz')
    fslreorient2std(expanded_func, preprocessPath + '/expanded_func.nii.gz')

    #let's navigate to the preprocess directory
    os.chdir(preprocessPath)

    #time for some brain extraction
    print("Starting BET.")
    struct_jid = bet('struct', 'struct_brain', m=True, f=0.1, submit={'queue': 'veryshort.q'})
    struct_fslanat_jid = bet('struct', 'struct_brain_biascorr', t="T1", betfparam=0.1)
    fmap_jid = bet('fmap_mag', 'fmap_mag_brain', submit={'queue': 'veryshort.q'})
    bet('expanded_func', 'expanded_func_brain', f=0.05, submit={'queue': 'veryshort.q'})

    #brain erode
    hold([fmap_jid])
    fmap_ero_jid = fslmaths('fmap_mag_brain').ero().run('fmap_mag_brain_ero')

    #prepare fieldmap images
    print("Preparing fieldmap image")
    fsl_prepare_fieldmap('fmap_phase.nii.gz', 'fmap_mag_brain_ero', 'fmap_rads', 1.02, submit={'queue': 'veryshort.q', 'j': fmap_ero_jid})

    os.chdir(dataDir)

    print("Closing script. Some jobs might be in the queue. Check brain extractions before proceeding. If all is good, run preprocessFeat.py.")

    #from here find the preprocess design file and start feat for preprocessing


