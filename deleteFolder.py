import os
from python_script_utils import get_subj_numbers
import shutil
import fsl.utils.assertions as asrt

dataDir = '/vols/Scratch/bnc208/friend_request_task'
print("This is the data directory: " + dataDir)

folderToBeDeleted = 'preprocessed_data.feat'

subj_number = get_subj_numbers()

for subj in subj_number:
    # Disable assertions
    asrt._DISABLE_ASSERTIONS = 1

    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)
    preprocessPath = subjPath + '/preprocessPy'
    print("Starting with: " + subjPath)

    os.chdir(subjPath)

    # Check if the directory to be deleted exists
    if os.path.exists(folderToBeDeleted):
        # Delete the directory
        shutil.rmtree(folderToBeDeleted)
        print(f"Deleted the directory: {folderToBeDeleted}")
    else:
        print(f"The directory: {folderToBeDeleted} does not exist.")







