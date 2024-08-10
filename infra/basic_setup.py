from pyinfra import host
from pyinfra.operations import apt, server


apt.update(
    name="Update apt repositories",
    _sudo=True,
)

apt.upgrade(
    name="Upgrade all packages",
    _sudo=True,
)

apt.packages(
    name="Ensure the essential tools are installed",
    packages=[
        "build-essential",
        "ruby-dev",
        "libssl-dev",
        "libpcap-dev",
        "net-tools",
        "zsh",
        "curl",
        "wget",
        "git",
        "vim",
        "screen",
        "tmux",
        "rsync",
    ],
    update=True,
    _sudo=True,
)


apt.packages(
    name="Ensure the basic utilities are installed",
    packages=[
        "silversearcher-ag",
        "htop",
        "ranger",
        "tree",
        "ncdu",
        "mtr",
        "jq",
    ],
    update=True,
    _sudo=True,
)


apt.packages(
    name="Ensure the python related dependecies are installed",
    packages=[
        "python3",
        "python3-dev",
        "python3-pip",
    ],
    update=True,
    _sudo=True,
)
