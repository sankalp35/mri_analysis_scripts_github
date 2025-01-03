#This file takes a template fsf file, modifies it for the current subject, and runs feat

import os
import shutil
from pathlib2 import Path

#Set data dir
dataDir = '/Users/sankalpgarud/Documents/friend_request_data/MRI_data/main_study_data'
print("This is the data directory: " +dataDir)


#Get template fsf
template_fsf = dataDir+'/designFSFs/design1.fsf'

#Subject names
subj_number = [1];

#create subject specific fsf and then place it in their folder
for subj in subj_number:
    subjName = '/S'+str(subj).zfill(2)
    subjPath = dataDir+subjName

    #copy fsf file into the subjects directory
    designFile = shutil.copyfile(template_fsf, subjPath+'/design1.fsf')

    #modify fsf file with subject specific paths
    path = Path(designFile)
    text = path.read_text()
    text = text.replace('SXX', subjName)
    path.write_text(text)

    #we should now be ready to run feat

    # create feat path if does not exists
    featPath = "/Users/sankalpgarud/Documents/friend_request_data/MRI_data/main_study_data/S01/design1.feat"
    doesExist = os.path.exists(featPath)
    if not doesExist:
        # Create a new directory because it does not exist
        os.makedirs(featPath)
        print("The new feat path is created!")

    os.chdir(subjPath)
    os.system('feat design1.fsf')
