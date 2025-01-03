import argparse
import subprocess
from fsl.wrappers.avwutils import fslmerge
from fsl.wrappers import fslreorient2std
import os
import shutil
from glob2 import glob
import fsl.utils.assertions as asrt

dataDir = '/vols/Scratch/bnc208/friend_request_task'
stage1Folder = 'd6_stage1_fslanat.feat'
tstat_prefix = '/d6_fslanatSynthstrip_stdspace_tstat'
subj_number = [2,3,5,7,9,10,11,12,13,14,15,16,17,19,20,21,22,23,30,26,27,28,29,6,8,24]

def process_tstats(tstat_numbers):
    tstat_numbers = list(map(int, tstat_numbers))

    for tstat_number in tstat_numbers:

        tstat_output_name = 'cmb_tstat_' + str(tstat_number) + stage1Folder

        tstat_output_path = os.path.join(dataDir, tstat_output_name + '.nii.gz')
        if os.path.exists(tstat_output_path):
            os.remove(tstat_output_path)
            print("Old combined tstat detected and deleted")

        subj_tstat_names = []
        for subj in subj_number:
            asrt._DISABLE_ASSERTIONS = 1

            subjPath = dataDir + '/S' + str(subj).zfill(2)
            subjStdtstat = subjPath + '/standard_cope'

            subjtstat = subjStdtstat+tstat_prefix+str(tstat_number).zfill(2)+'.nii.gz'
            print(subjtstat)

            os.chdir(dataDir)



            if os.path.exists(dataDir+'/'+tstat_output_name+'.nii.gz'):
                fslmerge('t', tstat_output_name, tstat_output_name, subjtstat)
            else:
                shutil.copyfile(subjtstat, tstat_output_name+'.nii.gz')

            subj_tstat_names.append(subjtstat)
        print(subj_tstat_names)

def main():
    parser = argparse.ArgumentParser(description="Process tstat numbers")
    parser.add_argument('tstat_numbers', nargs='+', help='One or more tstat numbers to process')
    args = parser.parse_args()
    process_tstats(args.tstat_numbers)

if __name__ == "__main__":
    main()
