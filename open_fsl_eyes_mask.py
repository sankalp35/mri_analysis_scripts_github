import subprocess
import os


dataDir = '/vols/Scratch/bnc208/friend_request_task'

file_paths = []
for subj in range(1, 31):
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    this_mask_path = subjPath+'/stage1ModDen.feat/reg_standard/mask.nii.gz'

    if os.path.exists(this_mask_path):
         file_paths.append(this_mask_path)

print(file_paths)

# Create the FSLeyes command
fsleyes_command = ["fsleyes"] + file_paths

# Run the command using subprocess
subprocess.run(fsleyes_command)
