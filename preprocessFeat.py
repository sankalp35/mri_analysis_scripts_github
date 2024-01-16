# Assuming brain extraction was successful, this step takes the prepared files and starts feat in verylong.q
# This file takes a template fsf, modifies it for the current subject, then starts pre-processing in verylong.q

import os
import shutil
from pathlib2 import Path
from fsl.data.image import Image
from fsl.data.featanalysis import loadFsf
from glob2 import glob
from python_script_utils import get_subj_numbers
import time

dataDir = '/vols/Scratch/bnc208/friend_request_task'

# grab the correct fsf
fsfName = 'preprocess_fslAnat_synthstrip_alterfB_intensityNormalisedFuncStructExpFunc_fullsearch.fsf'
templatePath = dataDir + '/templateFSF/' + fsfName
templatefsf_subj = '/S02'

output_folder_name = '/preprocessed_data_fslAnat_synthstrip_altref_intensityNormalisedStructAndFuncExpFunc_fullsearch'

subj_number = get_subj_numbers()

for subj in subj_number:
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName
    preprocessPath = subjPath + '/preprocessPy'

    # copy fsf file into the subjects directory
    designFile = shutil.copyfile(templatePath, subjPath + '/' + fsfName)

    # modify fsf file with subject specific paths
    path = Path(designFile)  # p here must be captial for the function.
    text = path.read_text()
    text = text.replace(templatefsf_subj, subjName)
    path.write_text(text)

    # Now, get the total number of timepoints from the func data
    fsfDict = loadFsf(designFile)  # loading fsf file to get image path
    func_path = fsfDict.get("feat_files(1)")
    old_npts = fsfDict.get("npts")
    print("Old npts: " + str(old_npts))

    # get npts of new image
    img = Image(func_path)
    new_npts = img.header.get("dim")[4]
    print("New npts: " + str(new_npts))

    # get old output dir and replace with new one
    old_output = fsfDict.get('outputdir')
    featPath = subjPath + output_folder_name
    print("Old Output Path: " + old_output)
    print("New Output Path: " + featPath)

    old_struct = fsfDict.get("highres_files(1)")
    potential_manual_struct = glob(preprocessPath + '/struct*manual*brain*nii*')

    # if not potential_manual_struct:  # if the list is empty
    # print("No manual struct found."+subjName)
    #  new_struct = old_struct
    #  else:
    # manual_struct = potential_manual_struct[0]
    # new_struct = manual_struct

    new_struct = old_struct
    print("Struct: " + old_struct)
    print("New Struct: " + new_struct)

    text = path.read_text()
    text = text.replace(str(old_npts), str(new_npts))
    text = text.replace(old_output, featPath)
    text = text.replace(old_struct, new_struct)
    path.write_text(text)

    # we should now be ready to run feat

    # # create feat path if it does not exist

    doesExist = os.path.exists(featPath + '.feat')
    if not doesExist:
        # Create a new directory because it does not exist
        print("No old preprocess folder detected")
    else:
        # if it already exists, then rewrite the original path
        shutil.rmtree(featPath + '.feat')
        print("The new feat path is created after deleting the old one")

    os.chdir(subjPath)
    os.system('FSLSUB_MEMORY_REQUIRED=40G feat ' + fsfName)
    print('Started pre-processing')
