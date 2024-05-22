import pyinfra
from pyinfra import host
from pyinfra.facts.server import User
from pyinfra.operations import apt, python, server

apt.update(
    name="Update apt repositories",
    _sudo=True,
)


def install_docker():
    # Install Docker
    apt.packages(
        name="Installing Docker",
        packages=["docker.io"],
        # apt-get install docker-ce docker-ce-cli containerd.io -y
        present=True,
        update=True,
        _sudo=True,
    )

    # Create docker group if not exist
    server.group(
        name="Create docker group",
        group="docker",
    )

    # Add user to docker group
    server.shell(
        name="Add current user to docker group",
        commands=[f"usermod -aG docker {host.get_fact(User)}"],
        _sudo=True,
    )

    # su -s server.user
    # Change docker.sock permission
    # server.shell(
    #     name="Change docker.sock permission",
    #     commands=["chmod 666 /var/run/docker.sock"],
    #     _sudo=True,
    # )

    # Restart docker daemon service
    server.shell(
        name="Restart docker daemon service",
        commands=["systemctl restart docker"],
        _sudo=True,
    )


python.call(
    name="Install Docker",
    function=install_docker,
)

server.shell(
    name="Execute some shell",
    commands=['echo "back to other operations!"'],
)
