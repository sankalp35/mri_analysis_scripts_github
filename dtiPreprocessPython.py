# File to pre process DTI data
from fsl.wrappers import fslroi, fslmaths, eddy, bet, topup, dtifit
from fsl.wrappers.flirt import flirt, applyxfm
from fsl.wrappers.fnirt import applywarp
import subprocess
from fsl.wrappers.avwutils import _fslmerge
import os
from glob2 import glob
import fsl.utils.assertions as asrt
import time




def fslmergeT(output, img1, img2, jobhold):
    completed_process = subprocess.run('fsl_sub -q veryshort.q -j ' +str(jobhold)+ ' fslmerge -t ' + output + ' ' + img1 + ' ' + img2)
    byte_str = completed_process.stdout
    jobid = int(byte_str.decode('utf-8').rstrip('\n')) #This may need to stay as a string
    return jobid


dataDir = '/vols/Scratch/bnc208/friend_request_task'
print("This is the data directory: " + dataDir)

#Subject names
subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
subj_number = int(subjInput)

#if the input is 99, then compute on all subjects
if subj_number == 99:
    subj_number = range(1, 31)
elif subj_number == 91:
    subjInputR = input("Start from which subject?: ") #camel R stands for range
    subj_number = range(int(subjInputR), 31)
    print("Working on: " + str(subj_number))
else:
    subj_number = [int(subjInput)]

for subj in subj_number:
    # Disable assertions
    asrt._DISABLE_ASSERTIONS = 1

    # Define where the subject specific raw files are stored
    subjPath = dataDir + '/S' + str(subj).zfill(2)
    preprocessPath = subjPath + '/preprocessPy'
    print("Starting with: " + subjPath)

    # Get diffusion files
    dwi = glob(subjPath + '/raw/*diff*AP*.nii')[0]
    dwiPA = glob(subjPath + '/raw/*diff*APrev*.nii')[0]
    bval = glob(subjPath + '/raw/*AP*.bval')[0]
    bvec = glob(subjPath + '/raw/*AP*.bvec')[0]

    # Get the b0 scan in AP and PA directions (first volume in time dimension is the b0 scan)
    fslroi(dwi, preprocessPath + '/AP_b0', 0, 1, submit={'q': 'veryshort.q'})
    roi_jid = fslroi(dwiPA, preprocessPath + '/PA_b0', 0, 1, submit={'q': 'veryshort.q'})

    os.chdir(preprocessPath)

    # Can't find fslmerge in fslpy so writing command line
    merge_id = fslmergeT('AP_PA_b0', 'AP_b0', 'PA_b0', roi_jid)
    print(merge_id)

    acqParamsPath = dataDir+'/'+'acqparamsDiff.txt'
    indexPath = dataDir+'/'+'index.txt'
    
    # Start TOPUP
    print("Files prepared. Starting with TOPUP")
    topup_jid = topup(imain='AP_PA_b0', datain=acqParamsPath, config='b02b0.cnf', out='topup_AP_PA_b0', iout='topup_AP_PA_b0_iout', fout='topup_AP_PA_b0_fout', submit={'queue': 'verylong.q', 'jobhold': merge_id})

    # prepare for eddy
    fslmergeT('dwiForEddy', dwi, dwiPA, roi_jid)
    fslmergeT('ap_pa_ap_pa_b0', 'AP_PA_b0', 'AP_PA_b0', topup_jid)
    os.system('paste '+bval+' '+bval+' > twoBval.bval')
    os.system('paste '+bvec+' '+bvec+' > twoBvec.bvec')


    # prepare mask for eddy
    # no dif stands for no diffusion image (extracted 1st vol from diffusion image)
    fslmaths_jid = fslmaths('topup_AP_PA_b0_iout').Tmean().run('hifi_nodif', submit={'queue': 'veryshort.q', 'jobhold': topup_jid})
    bet_jid = bet(input='hifi_nodif', output='hifi_nodif_brain', m=True, f=0.1, submit={'queue': 'veryshort.q', 'jobhold': fslmaths_jid})


    eddy_jid = eddy(imain='dwiForEddy.nii.gz', mask='hifi_nodif_brain_mask.nii.gz', index=indexPath, acqp=acqParamsPath, bvecs='twoBvec.bvec',
                  bvals='twoBval.bval', fwhm=0, topup='topup_AP_PA_b0', flm='quadratic',
                  out='eddy_unwarped_images', data_is_shelled=True, submit={'queue': 'bigmem.q', 'jobhold': bet_jid}) #removed resamp='lsr'


    # os.system('eddy --imain=dwiForEddy.nii.gz \
    #  --mask=hifi_nodif_brain_mask \
    #  --index=index.txt \
    #  --acqp=acqparamsDiff.txt \
    #  --bvecs=twoBvec.bvec\
    #  --bvals=twoBval.bval\
    #  --fwhm=0 \
    #  --topup=topup_AP_PA_b0 \
    #  --flm=quadratic \
    #  --out=eddy_unwarped_images \
    #  --data_is_shelled')
    #start dtifit
    print("Starting DTI fit")

   # os.system('dtifit --data=eddy_unwarped_images --mask=hifi_nodif_brain_mask --bvecs=twoBvec.bvec --bvals=twoBval.bval --out=dti')
    dti_jid = dtifit(data='eddy_unwarped_images', mask='hifi_nodif_brain_mask', bvecs='twoBvec.bvec', bvals='twoBval.bval', out='dti', submit={'queue': 'verylong.q', 'jobhold': eddy_jid})

    #Transform dti data to standard space
    flirtref='preprocessed_data.feat/reg/highres'
    flirt_jid = flirt(src='hifi_nodif_brain.nii.gz', ref=flirtref, out='hifi_nodif_reg_tohighres', omat='dtiToHighres', submit={'q': 'verylong.q', 'jobhold': dti_jid})
    xfm_jid = applyxfm(src='dti_FA.nii.gz', ref=flirtref, mat='dtiToHighres', out='dti_FA2highres', submit={'q': 'veryshort.q', 'jobhold': flirt_jid})
    applywarp(src='dti_FA2highres.nii.gz', ref='/opt/fmrib/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz', out='fa2highres2mni', w='highres2standard_warp.nii.gz', submit={'q': 'bigmem.q', 'jobhold': xfm_jid})
