from pyinfra import host
from pyinfra.operations import apt, server


# Install Docker
apt.packages(
    name="Install Docker",
    packages=["docker.io"],
    # apt-get install docker-ce docker-ce-cli containerd.io -y
    present=True,
    update=True,
    _sudo=True,
)


# Install Kind
server.shell(
    name="Install Kind",
    commands=[
        "curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64",
        "chmod +x ./kind",
        "mv ./kind /usr/local/bin/kind",
    ],
    _sudo=True,
)
