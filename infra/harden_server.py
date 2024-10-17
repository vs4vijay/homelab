from pyinfra import host
from pyinfra.operations import apt, server


# Change SSH port to 22222
server.shell(
    name='Change SSH port',
    commands=[
        'sed -i "s/#Port 22/Port 22222/" /etc/ssh/sshd_config',
        # 'systemctl restart sshd',
    ],
)

# Disable password authentication and allow only public key authentication
server.shell(
    name='Disable password authentication',
    commands=[
        'sed -i "s/#PasswordAuthentication yes/PasswordAuthentication no/" /etc/ssh/sshd_config',
        # 'systemctl restart sshd',
    ],
)

# Disable root login
server.shell(
    name='Disable root login',
    commands=[
        'sed -i "s/#PermitRootLogin prohibit-password/PermitRootLogin no/" /etc/ssh/sshd_config',
        # 'systemctl restart sshd',
    ],
)

# Restart SSH
server.shell(
    name='Restart SSH Server',
    commands=[
        'systemctl restart sshd',
    ],
)
