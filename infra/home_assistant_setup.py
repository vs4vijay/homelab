from pyinfra import local, host
from pyinfra.operations import apt, files, systemd

# Install required packages
apt.packages(
    {"Install required packages"},
    ["python3", "python3-pip", "python3-venv", "git"],
    update=True,
    sudo=True,
    host=host,
)

# Create a virtual environment
with files.directory("/opt/homeassistant", sudo=True, host=host):
    local.shell("python3 -m venv .venv", sudo=True, host=host)

# Activate the virtual environment
with files.directory("/opt/homeassistant", sudo=True, host=host):
    local.shell("source venv/bin/activate", sudo=True, host=host)

# Clone the Home Assistant repository
with files.directory("/opt/homeassistant", sudo=True, host=host):
    local.shell(
        "git clone https://github.com/home-assistant/core.git --depth 1", sudo=True, host=host
    )

# Install Home Assistant dependencies
with files.directory("/opt/homeassistant/core", sudo=True, host=host):
    local.shell("pip3 install -r requirements.txt", sudo=True, host=host)

# Create a systemd service for Home Assistant
systemd.service(
    {"Create systemd service for Home Assistant"},
    "home-assistant",
    "/opt/homeassistant/core",
    ".venv/bin/hass",
    sudo=True,
    host=host,
)

# Enable and start the Home Assistant service
systemd.service(
    {"Enable and start Home Assistant service"},
    "home-assistant",
    running=True,
    enabled=True,
    sudo=True,
    host=host,
)
