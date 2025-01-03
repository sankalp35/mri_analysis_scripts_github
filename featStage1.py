
import os
import shutil
from pathlib2 import Path
from fsl.data.image import Image
from fsl.data.featanalysis import loadFsf
from python_script_utils import get_subj_numbers

dataDir = '/vols/Scratch/bnc208/friend_request_task/'

designName = 'd8_noITI_ppi_stage1_fslanat' #mostly used for the fsf file
template_subj_name = 'S02'

#Grab a template
templatePath = dataDir+'/templateFSF/'+designName+'.fsf'

subj_number = get_subj_numbers()

for subj in subj_number:
    subjName = 'S'+str(subj).zfill(2)
    subjPath = dataDir+subjName+'/'

    #copy stage1 design file to the subject folder
    designFile = shutil.copyfile(templatePath, subjPath + designName+'.fsf')

    # modify fsf file with subject specific paths
    path = Path(designFile)  # p here must be captial for the function.
    text = path.read_text()

    text = text.replace(template_subj_name, subjName)

    path.write_text(text) #This is important to get values relevant to this subject

    text = path.read_text()
    # Now, get the total number of timepoints from the func data
    fsfDict = loadFsf(designFile)  # loading fsf file to get image path
    func_path = fsfDict.get("feat_files(1)")
    print(func_path)

    old_npts = fsfDict.get("npts")
    print("Old npts: "+str(old_npts))

    #get npts of new image
    img = Image(func_path)
    new_npts = img.header.get("dim")[4]
    print("New npts: " + str(new_npts))

    #get old output dir and replace with new one
    old_output = fsfDict.get('outputdir')
    new_output = subjPath+designName
    print("Old Output Path: "+old_output)
    print("New Output Path: "+new_output)

    text = text.replace(str(old_npts), str(new_npts))
    text = text.replace(old_output, new_output)

    path.write_text(text)
    #we should now be ready to run feat

    os.chdir(subjPath)

    first_level_folder = new_output+".feat"
    #Remove previous folder by the same name it already exists
    if os.path.exists(first_level_folder):
        print(f"Folder {first_level_folder} exists.")
        # delete the folder
        shutil.rmtree(first_level_folder)
        print(f"Folder {first_level_folder} deleted.")
    else:
        print(f"Folder {first_level_folder} does not exist.")

    os.system('fsl_sub -q verylong.q -T 360 -R 30 feat '+designName+'.fsf')
    print('Started first level analysis for subject ' + subjName)