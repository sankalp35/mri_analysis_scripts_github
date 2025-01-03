#This file queries a feat directory
# I am here checking if the regressors are fine, especially the outcome regressor

from fsl.data.featdesign import loadDesignMat, FEATFSFDesign

feat_folder = '/Users/sankalpgarud/Documents/friend_request_data/MRI_data/main_study_data/S10/d6_stage1_fslanat.feat/'

design = FEATFSFDesign(feat_folder)

loadDesignMat(feat_folder)