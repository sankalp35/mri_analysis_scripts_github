import sys
import numpy as np
from fsl.data.image import Image


def normalize_intensity(image_data):
    max_intensity = np.max(image_data)
    normalized_data = image_data / max_intensity
    return normalized_data


def main(input_file, output_file):
    # Load the input functional MRI image
    img = Image(input_file)
    img_data = img.data

    # Intensity normalize the fMRI image data
    normalized_data = normalize_intensity(img_data)

    # Create a new Image with the normalized data and save it
    normalized_img = Image(normalized_data, header=img.header, xform=img.voxToWorldMat)
    normalized_img.save(output_file)
    print(f"Intensity normalization completed. Saved to {output_file}")


    if len(sys.argv) != 3:
        print("Usage: python intensity_normalization.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)
