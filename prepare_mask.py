import argparse
import subprocess


def apply_warp(input_mask, output_mask):
    reference_image = "/opt/fmrib/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz"
    command = ["applywarp", "-i", input_mask, "-o", output_mask, "-r", reference_image]

    try:
        subprocess.run(command, check=True)
        print("Warp transformation applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error encountered while applying warp transformation: {e}")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Apply warp transformation to a mask.")
    parser.add_argument("mask_name", help="Input mask name")
    args = parser.parse_args()

    # Set input and output mask filenames
    input_mask = args.mask_name + ".nii.gz"
    output_mask = args.mask_name + "_1mm.nii.gz"

    # Apply warp transformation
    apply_warp(input_mask, output_mask)
