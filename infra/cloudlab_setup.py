import pyinfra
from pyinfra import host
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


python.call(
    name="Install Docker",
    function=install_docker,
)


server.shell(
    name="Execute some shell",
    commands=['echo "back to other operations!"'],
)
