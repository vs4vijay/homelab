from pyinfra.operations import apt

apt.packages(
    name="Ensure wget is installed",
    packages=['wget'],
    update=True,
    _sudo=True,
)