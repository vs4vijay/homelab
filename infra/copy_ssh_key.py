import subprocess

# Define the target servers
source_server = 'source_server'
destination_server = 'destination_server'

# SSH command to list public keys on the source server
list_keys_command = f'ssh {source_server} "cat ~/.ssh/authorized_keys"'

# Execute the command and capture the output
output = subprocess.check_output(list_keys_command, shell=True, universal_newlines=True)

# Split the output into individual keys
keys = output.strip().split('\n')

# Display the keys to the user
print('Available public keys:')
for i, key in enumerate(keys):
    print(f'{i+1}. {key}')

# Prompt the user to choose a key
selected_key_index = int(input('Enter the number of the key to copy: ')) - 1
selected_key = keys[selected_key_index]

# SSH command to copy the selected key to the destination server
copy_key_command = f'ssh {destination_server} "echo \'{selected_key}\' >> ~/.ssh/authorized_keys"'

# Execute the command to copy the key
subprocess.run(copy_key_command, shell=True)