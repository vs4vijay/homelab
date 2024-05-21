from pyinfra import local, host
from pyinfra.operations import files, ssh

# Define the target host
target_host = host


# Generate the SSH key pair locally
local.shell('ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa1')

# Copy the public key to the target host
ssh.authorized_key(
    name="Copy SSH public key",
    user=target_host.user,
    key="~/.ssh/id_rsa1.pub",
)
