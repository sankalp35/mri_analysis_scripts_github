import os
import subprocess
import argparse

# Define standard brain path here
standard_brain = '/usr/local/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz'

# Define list of color maps to cycle through
positive_cmaps = ['red-yellow', 'hot', 'copper']
negative_cmaps = ['blue-lightblue', 'cool', 'green']

def open_zstat_in_fsleyes(feat_dir, cope_nums, cont_num):
    cmd = ['fsleyes', standard_brain]

    for i, cope_num in enumerate(cope_nums):
        # Construct path to zstat file
        for j, cont in enumerate(cont_num):
            zstat_file_path = os.path.join(feat_dir, f'cope{cope_num}.feat/stats/zstat{cont}.nii.gz')

        # Select color maps from lists
        positive_cmap = positive_cmaps[i % len(positive_cmaps)]
        negative_cmap = negative_cmaps[i % len(negative_cmaps)]

        # Extend command to add this cope to the FSLeyes display
        cmd.extend([zstat_file_path, '-cm', positive_cmap, '-nc', negative_cmap, '-dr', '3', '3.5', '-n', f'cope{cope_num}'])

    # Run command to open FSLeyes with all copes
    subprocess.run(cmd)

if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser(description='Open zstat1.nii.gz file in FSLeyes.')
    parser.add_argument('--feat_dir', required=True, help='Path to FEAT directory')
    parser.add_argument('--cope', type=int, nargs='+', required=True, help='List of COPE numbers')
    parser.add_argument('--cont', type=int, nargs='+', required=True, help='Which Zstat do you wish to open?')
    args = parser.parse_args()
    print(args.cope)

    open_zstat_in_fsleyes(args.feat_dir, args.cope, args.cont)
