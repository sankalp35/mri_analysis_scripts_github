2024 - Sankalp Garud

This is a repository written for MRI analysis using fsl(py) and synthstrip, and is optimised for 7T data and optimised for the fmrib cluster.

Here is a brief description of what the files do:

prepareforPreprocess.py: This will reorient structural, functional, and bias fields to standard. Will create a fieldmap and brain extract. 

prepareForPreprocess_improved_fslanat_synthstrip.py: We noticed that the conventional brain extraction using BET did not work very well for 7T data. This script uses synthstrip to extract the brain which worked better for 7T data. It also has options for bias correcting the structural and for registering the mask created by synthstrip to the functional. This mask can be used in the first stage feat instead of the default fsl mask.

featStage1: Undertakes first level feat analysis using a template fsf file

(for stage 2 I just use the feat gui)

tstat2std_d6.py: registers tstat images to standard space and extracts mean timeseries from given ROIs

Other utilities:

biasCorrPy_batch.py: bias corrects the functionals

transfer_local2jalapeno_file.py: transfers a file from local to jalapeno. this sidesteps use of terminal or cyberduck to transfer files

transfer_local2jalapeno.py: same as above but for the entire folder

python_script_utils.py: contains a couple of options for selecting subjects to run analysis on