import paramiko
import os
import shutil

hostname = 'jalapeno.fmrib.ox.ac.uk'
username = 'bnc208'
password = 'jnZm4a7ZBeyveSnR'

dataDir_local = '/Users/sankalpgarud/Documents/friend_request_data/MRI_data/main_study_data/'
dataDir_remote = '/vols/Scratch/bnc208/friend_request_task/'

design_folder = 'd3_first12_split_intensityNormalisedStructFuncExpFunc_noFmapCorr_fullsearch.feat'
design_file = 'design.mat'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username=username, password=password)

print("Logged in to server ;)")

sftp = ssh.open_sftp()

# Loop over all your MRI data folders
for i in range(2, 31):
    # skip S18 and S25 as per your initial list
    if i not in [18, 25]:
        folder_name = f"S{i:02d}"
        remote_file_path = os.path.join(dataDir_remote, folder_name, design_folder, design_file)
        local_file_path = os.path.join(dataDir_local, folder_name, design_folder, design_file)

        # Create local directory structure if it doesn't exist
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Check if the remote file exists
        try:
            sftp.stat(remote_file_path)
        except FileNotFoundError:
            print(f"File {remote_file_path} does not exist on the remote server, skipping...")
            continue

        # Check if the local path is a directory
        if os.path.isdir(local_file_path):
            print(f"Local path {local_file_path} is a directory, deleting it...")
            shutil.rmtree(local_file_path)

        # Download the file
        print(f"Downloading {remote_file_path} to {local_file_path}")
        sftp.get(remote_file_path, local_file_path)

sftp.close()
ssh.close()

print('File transfer complete.')
