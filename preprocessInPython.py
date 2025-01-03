from fsl.wrappers import fslreorient2std, bet, fslmaths, fsl_prepare_fieldmap
import os
from glob2 import glob

dataDir = '/Users/sankalpgarud/Documents/friend_request_data/MRI_data/main_study_data'


print("This is the data directory: " +dataDir)

os.chdir(dataDir)

#Subject names
subj_number = [1];

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
    structural = glob(subjPath+'/raw/*struct*')[0]
    func = glob(subjPath+'/raw/*func*')[0]
    fmap_mag = glob(subjPath+'/raw/*field*1001*')[0]
    fmap_phase = glob(subjPath+'/raw/*field*2001*')[0]

    #Reorient everything to standard
    fslreorient2std(structural, preprocessPath+'/struct.nii.gz')
    #fslreorient2std(func, preprocessPath+'/func.nii.gz')
    fslreorient2std(fmap_mag, preprocessPath+'/fmap_mag.nii.gz')
    fslreorient2std(fmap_phase, preprocessPath+'/fmap_phase.nii.gz')

    #let's navigate to the preprocess directory
    os.chdir(preprocessPath)

    #time for some brain extraction
    print("Starting BET")
    bet('struct', 'struct_brain', m=True, f=0.05)
    bet('fmap_mag', 'fmap_mag_brain')

    #brain erode
    fslmaths('fmap_mag_brain').ero().run('fmap_mag_brain_ero')

    #prepare fieldmap images
    print("Preparing fieldmap image")
    fsl_prepare_fieldmap('fmap_phase.nii.gz', 'fmap_mag_brain_ero', 'fmap_rads', 1.02)

    #the way to open fsl is through these system commands
    os.system("fsleyes struct_brain")

    os.chdir(dataDir)

    #from here find the preprocess design file and start feat for preprocessing





