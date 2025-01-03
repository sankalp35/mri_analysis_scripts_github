from fsl.wrappers.fast import fast

def correct_bias_field(input_image, output_image, num_classes=2):
    """
    Corrects for bias field in an fMRI image using FSL's FAST algorithm.

    :param input_image: str, path to the input fMRI image (e.g., 'input_image.nii.gz')
    :param output_image: str, path to the corrected output image (e.g., 'output_image.nii.gz')
    :param num_classes: int, number of tissue-type classes (default: 2)
    """
    fast(input_image, output_image, B=True, submit={'queue':'short.q'})


if __name__ == '__main__':
    input_image = '/vols/Scratch/bnc208/friend_request_task/S01/preprocessPy/func.nii.gz'
    output_image = 'output_image_biascorr.nii.gz'

    correct_bias_field(input_image, output_image)
