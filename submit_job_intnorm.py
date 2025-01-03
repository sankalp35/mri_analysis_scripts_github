import os
import sys


def main(input_file, output_file):
    job_command = f"python intensity_normalization.py {input_file} {output_file}"
    submission_command = f"fsl_sub -q veryshort.q '{job_command}'"
    os.system(submission_command)
    print("Job submitted to FSL cluster.")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python submit_job.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
