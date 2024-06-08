from pyinfra import host
from pyinfra.operations import apt, server


# Update

# Install guacamole

# Add apt repository
apt.repo(
    name='Add Guacamole PPA',
    src='ppa:guacamole/stable',
    _sudo=True,
)

# Install guacamole
apt.packages(
    name='Install Guacamole',
    packages=['guacamole-tomcat'],
    update=True,
    _sudo=True,
)