import paramiko
import os

hostname = 'jalapeno.fmrib.ox.ac.uk'
username = 'bnc208'
password = 'jnZm4a7ZBeyveSnR'

dataDir_local = '/Users/sankalpgarud/Documents/friend_request_data/MRI_data/'
dataDir_remote = '/vols/Scratch/bnc208/'

file_name = 'transferReg.py'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(hostname=hostname, username=username, password=password)
print("Logged in to server ;)")
sftp = ssh.open_sftp()

file_path_local = dataDir_local + file_name

file_path_remote = dataDir_remote + file_name

print(f"Local file path: {file_path_local}")
print(f"Remote file path: {file_path_remote}")
print(f"Local file size: {os.path.getsize(file_path_local)}")

with open(file_path_local, "rb") as local_file:
    data = local_file.read()
    with sftp.open(file_path_remote, "wb") as remote_file:
        remote_file.write(data)

sftp.close()
ssh.close()

print('File transfer complete.')
