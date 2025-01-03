# runs pnm stage 1 and stage 2

import shutil
import subprocess

from fsl.wrappers import fslreorient2std, fsl_anat, fslmaths, fsl_prepare_fieldmap, applywarp, flirt, applyxfm
import fsl_sub
from fsl.utils.run import hold
import os
from glob2 import glob
from python_script_utils import get_subj_numbers
from fsl.wrappers.wrapperutils import fslwrapper, applyArgStyle


# Custom pnmPy function
# only needs input file
@fslwrapper
def pnm_stage1(input_biopac_txt, **kwargs):
    cmd = ['pnm_stage1', '-i', input_biopac_txt, '-o', "pnmPy", '-s', '200', '--tr=2.033',
           '--smoothcard=0.1', '--smoothresp=0.1', '--resp=1', '--cardiac=2', '--trigger=3', '--rvt']
    return cmd + applyArgStyle('-=', **kwargs)


# this should only need input func
@fslwrapper
def pnm_evs(input_func, **kwargs):
    cmd = ['pnm_evs', '-i', input_func, '-c', "pnmPy_card.txt",
           '-r', "pnmPy_resp.txt", '-o', "pnmPy",
           '--tr=2.033',
           '--rvt=pnmPy_rvt.txt', '--rvtsmooth=10',
           '--slicetiming=/vols/Scratch/bnc208/friend_request_task/slice_timing_new.txt',
           '--or=4', '--oc=4', '--multc=2', '--multr=2']
    return cmd + applyArgStyle('-=', **kwargs)


@fslwrapper
def fslFixText(input_txt, output_txt, **kwargs):
    cmd = ['fslFixText', input_txt, output_txt]
    return cmd + applyArgStyle('-=', **kwargs)

def generate_evlist(path2pnm):
    # Generate list of nifi files
    nifis = imglob(os.listdir(path2pnm))
    # Generate the strings to be written to the file
    lines = [f"{path2pnm}/{item}.nii.gz" for item in nifis]
    # Write the generated lines to the output file
    with open(f"{path2pnm}/out_evlist.txt", "w") as file:
        for line in lines:
            file.write(line + "\n")


# directory of the data
dataDir = '/vols/Scratch/bnc208/friend_request_task'
preprocessFolder = '/preprocessed_data_fslAnat_synthstrip_altref_intensityNormalisedStructAndFuncExpFunc_fullsearch.feat'

# get subject numbers to loop over
subj_number = get_subj_numbers()

for subj in subj_number:
    subjName = '/S' + str(subj).zfill(2)
    subjName_txt = 'S' + str(subj).zfill(2)
    subjPath = dataDir + subjName
    beh_path = subjPath + '/behavioural'

    os.chdir(beh_path)

    print("Starting in: " + beh_path)

    # get biopac text file
    biopac = glob('biopac*txt')[0]
    print("Found biopac file: " + biopac)

    if not os.path.exists("physio_fixed.txt"):
        print("Creating fixed biopac file from fslFixText")
    fslFixText(biopac, "physio_fixed.txt")

    input_biopac_txt = "physio_fixed.txt"
    pnm_jid = pnm_stage1(input_biopac_txt, submit={'queue': 'short.q'})

    # get filtered func from preprocessing
    func = subjPath + preprocessFolder + '/filtered_func_data.nii.gz'
    # run stage 2
    pnm_evs(func, submit={'jobhold': pnm_jid, 'queue': 'short.q'})

    #simone script
    pnmevs_jid = pnm_evs(func, submit={'queue': 'short.q'})
    hold([pnmevs_jid])
    generate_evlist(pnmPath)