import argparse
import subprocess
from fsl.wrappers.avwutils import fslmerge
from fsl.wrappers import fslreorient2std
import os
import shutil
from glob2 import glob
import fsl.utils.assertions as asrt

dataDir = '/vols/Scratch/bnc208/friend_request_task'
stage1Folder = '/d6_stage1.feat'
subj_number = [2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24,26,27,28,29,30]

def process_copes(cope_numbers):
    cope_numbers = list(map(int, cope_numbers))

    for cope_number in cope_numbers:

        cope_output_name = 'cmb_cope_' + str(cope_number)

        cope_output_path = os.path.join(dataDir, cope_output_name + '.nii.gz')
        if os.path.exists(cope_output_path):
            os.remove(cope_output_path)
            print("Old combined cope detected and deleted")

        subj_cope_names = []
        for subj in subj_number:
            asrt._DISABLE_ASSERTIONS = 1

            subjPath = dataDir + '/S' + str(subj).zfill(2)
            subjStdCope = subjPath + '/standard_cope'

            subjcope = subjStdCope+'/d6_stdspace_cope'+str(cope_number).zfill(2)+'.nii.gz'
            print(subjcope)

            os.chdir(dataDir)



            if os.path.exists(dataDir+'/'+cope_output_name+'.nii.gz'):
                fslmerge('t', cope_output_name, cope_output_name, subjcope)
            else:
                shutil.copyfile(subjcope, cope_output_name+'.nii.gz')

            subj_cope_names.append(subjcope)
        print(subj_cope_names)

def main():
    parser = argparse.ArgumentParser(description="Process cope numbers")
    parser.add_argument('cope_numbers', nargs='+', help='One or more cope numbers to process')
    args = parser.parse_args()
    process_copes(args.cope_numbers)

if __name__ == "__main__":
    main()
