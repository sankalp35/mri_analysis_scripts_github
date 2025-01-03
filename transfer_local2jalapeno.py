#Transfers "folder_name" from subject specific directory locally to jalapeno
import paramiko
import os


hostname = 'jalapeno.fmrib.ox.ac.uk'
username = 'bnc208'
password = 'jnZm4a7ZBeyveSnR'

dataDir_local = '/Users/sankalpgarud/Documents/friend_request_data/MRI_data/main_study_data/'
dataDir = '/vols/Scratch/bnc208/friend_request_task/'
folder_name = 'd8_noITI_evs'

# Create an SSH client object
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the SSH server
ssh.connect(hostname=hostname, username=username, password=password)

# Create an SFTP client object
sftp = ssh.open_sftp()

for subj in range(1, 31):
    subjName = '/S' + str(subj).zfill(2)
    subjPath = dataDir + subjName

    #define local and remote paths
    local_path = dataDir_local+subjName+'/'+folder_name
    remote_path = dataDir+subjName+'/'+folder_name

    try:
        sftp.chdir(remote_path)  # Test if remote_path exists
        print("Remote path exists")
    except IOError:
        sftp.mkdir(remote_path)  # Create remote_path
        sftp.chdir(remote_path)
        print("Remote path created")

    for (root, dirs, files) in os.walk(local_path, topdown=True):
        for file in files:
            file_path_local = local_path + '/' + file
            file_path_remote = remote_path + '/' + file
            sftp.put(file_path_local, file_path_remote)
            print(subjName)

# Close the SFTP and SSH connections
sftp.close()
ssh.close()

print('File transfer complete.')