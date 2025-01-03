#This file prepares a template fsf for a higher level analysis and then starts feat

import os
import shutil
from pathlib2 import Path
from fsl.data.image import Image
from fsl.data.featanalysis import loadFsf
from glob2 import glob
import time

dataDir = '/vols/Scratch/bnc208/friend_request_task'

#designName
lowerLevelFeat = 'd3_first12_split_intensityNormalisedStructFunc_noFmapCorr.feat'
higherLevelFeatOutput ='higher_level_d3_first12_split_intensityNormalisedStructFunc_noFmapCorr'


#Higher level template fsf
templatePath = dataDir+'/templateFSF/highlevelfeats_26.fsf'

#New template name
newTemplatePath = dataDir+'/templateFSF/higherlevelfeats_26_d3_first12_split_intensityNormalisedStructFunc_noFmapCorr.fsf'

# copy stage1 design file to the subject folder
designFile = shutil.copyfile(templatePath, newTemplatePath)

# modify fsf file with subject specific paths
path = Path(designFile)  # p here must be captial for the function.
text = path.read_text()

text = text.replace('d3_first12_split.feat', lowerLevelFeat)
text = text.replace('12split_26ppl', 'friend_request_task/'+higherLevelFeatOutput)

path.write_text(text)

os.system("feat "+newTemplatePath)





