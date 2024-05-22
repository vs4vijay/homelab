from pyinfra import local, host, logger
from pyinfra.operations import files, ssh
import select

# Define the target host
target_host = host


logger.info("Select the SSH key to copy to the target host")

# List all local keys
local_keys = local.shell("ls ~/.ssh/*.pub", splitlines=True)

logger.info("Available keys:", local_keys.output)


# Ask user to select which key to add to authorized keys
selected_key_index = input(
    "Select the key to add to authorized keys (0 to generate new key): "
)

if selected_key_index == "0":
    # Generate a new SSH key pair locally
    result = local.shell('ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa1')

    print(result.stdout)

    selected_key = "~/.ssh/id_rsa1.pub"
else:
    # Get the selected key based on the index
    selected_key = local_keys[int(selected_key_index) - 1]


logger.info(f"Selected key: {selected_key}")

# Copy the selected key to the target host
# ssh.authorized_key(
#     name="Copy SSH public key",
#     user=target_host.user,
#     key=selected_key,
# )


# Copy the selected key to the target host
# ssh.authorized_key(
#     name="Copy SSH public key",
#     user=target_host.user,
#     key=f"~/.ssh/{selected_key}",
# )

# Generate the SSH key pair locally
# local.shell('ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa1')

logger.info("Copying SSH key to the target host")


# Copy the public key to the target host
# ssh.authorized_key(
#     name="Copy SSH public key",
#     user=target_host.user,
#     key="~/.ssh/id_rsa1.pub",
# )
