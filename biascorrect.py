import sys
import os


def bias_correction_fsl(input_image_path, output_image_path):
    # Check if input file exists
    if not os.path.exists(input_image_path):
        print(f"Input image file '{input_image_path}' does not exist.")
        sys.exit(1)

    # Create output directory if it does not exist
    output_dir = os.path.dirname(output_image_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare command for FSL's FAST bias correction
    output_basename = os.path.splitext(output_image_path)[0]
    command = f"fsl_sub fast -B -t 2 -b -o {output_basename} {input_image_path}"

    # Run the command
    os.system(command)

def bias_correct_fslmath(functional, bias_field, output):
    if not os.path.exists(functional):
        print(f"Input functional file '{functional}' does not exist.")
        sys.exit(1)

    if not os.path.exists(bias_field):
        print(f"Input bias file '{bias_field}' does not exist.")
        sys.exit(1)

    command = f"fsl_sub fslmaths {functional} -div {bias_field} {output}"

    # Run the command
    os.system(command)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python biascorrect.py <input_image_path> <output_image_path>")
        sys.exit(1)

    input_image_path = sys.argv[1]
    output_image_path = sys.argv[2]

    bias_correction_fsl(input_image_path, output_image_path)
