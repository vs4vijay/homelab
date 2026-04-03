import shlex

from pyinfra import logger
from pyinfra.operations import apt, server


expected_public_ip = input(
	"Enter the expected public IP for this host to confirm the Proxmox install target: "
).strip()

if not expected_public_ip:
	raise SystemExit("Expected public IP is required to continue.")

expected_public_ip_shell = shlex.quote(expected_public_ip)


apt.update(
	name="Update apt repositories",
	_sudo=True,
)

apt.packages(
	name="Ensure Proxmox installation prerequisites are installed",
	packages=[
		"ca-certificates",
		"curl",
		"gpg",
		"wget",
	],
	_sudo=True,
)

server.shell(
	name="Validate Proxmox target platform",
	commands=[
		(
			'set -eu; '
			'. /etc/os-release; '
			'arch="$(dpkg --print-architecture)"; '
			'case "$arch" in '
			'  amd64) ;; '
			'  arm64|armhf|aarch64) '
			'    echo "ARM is not supported for Proxmox VE here. Use PXVIRT instead:" >&2; '
			'    echo "https://github.com/jiangcuo/pxvirt" >&2; '
			'    echo "https://docs.pxvirt.lierfang.com/en/installfromdebian.html" >&2; '
			'    exit 1 ;; '
			'  *) echo "Unsupported architecture: $arch" >&2; exit 1 ;; '
			'esac; '
			'if [ "$ID" != "debian" ] && ! printf "%s" "${ID_LIKE:-}" | grep -qw debian; then '
			'  echo "This deploy supports Debian-based systems only." >&2; '
			'  exit 1; '
			'fi; '
			'if [ "${VERSION_CODENAME:-}" != "trixie" ]; then '
			'  echo "This deploy targets Debian 13 Trixie." >&2; '
			'  exit 1; '
			'fi'
		),
	],
	_sudo=True,
)

server.shell(
	name="Validate hostname resolves to a non-loopback IP",
	commands=[
		(
			'set -eu; '
			'resolved_ip="$(hostname --ip-address | awk "{print $1}")"; '
			'if [ -z "$resolved_ip" ] || printf "%s" "$resolved_ip" | grep -Eq "^(127\\.|::1$)"; then '
			'  echo "Hostname resolves to a loopback or empty address. Fix /etc/hosts or DNS before installing Proxmox VE." >&2; '
			'  exit 1; '
			'fi'
		),
	],
	_sudo=True,
)

server.shell(
	name="Confirm detected public IP matches the expected Proxmox target",
	commands=[
		(
			'set -eu; '
			'public_ip="$(curl -4fsSL https://api.ipify.org || curl -fsSL https://ifconfig.me)"; '
			'if [ -z "$public_ip" ]; then '
			'  echo "Unable to detect a public IP from a public service." >&2; '
			'  exit 1; '
			'fi; '
			"if [ \"$public_ip\" != "
			+ expected_public_ip_shell
			+ ' ]; then '
			'  echo "Detected public IP $public_ip does not match expected IP '
			+ expected_public_ip
			+ '." >&2; '
			'  exit 1; '
			'fi; '
			'echo "Confirmed public IP: $public_ip"'
		),
	],
	_sudo=False,
)

server.shell(
	name="Install the Proxmox VE repository key and source",
	commands=[
		"install -d -m 0755 /usr/share/keyrings",
		(
			"wget -qO /usr/share/keyrings/proxmox-archive-keyring.gpg "
			"https://enterprise.proxmox.com/debian/proxmox-archive-keyring-trixie.gpg"
		),
		(
			"cat > /etc/apt/sources.list.d/pve-install-repo.sources <<'EOF'\n"
			"Types: deb\n"
			"URIs: http://download.proxmox.com/debian/pve\n"
			"Suites: trixie\n"
			"Components: pve-no-subscription\n"
			"Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg\n"
			"EOF"
		),
	],
	_sudo=True,
)

server.shell(
	name="Upgrade the system and install the Proxmox kernel",
	commands=[
		(
			'set -eu; '
			'DEBIAN_FRONTEND=noninteractive apt-get update; '
			'DEBIAN_FRONTEND=noninteractive apt-get full-upgrade -y; '
			'if uname -r | grep -q -- "-pve"; then '
			'  echo "Already running a Proxmox kernel."; '
			'else '
			'  DEBIAN_FRONTEND=noninteractive apt-get install -y proxmox-default-kernel; '
			'  echo "Installed proxmox-default-kernel. Reboot into the new kernel and rerun this deploy to complete package installation."; '
			'fi'
		),
	],
	_sudo=True,
)

server.shell(
	name="Install Proxmox VE packages after booting into the Proxmox kernel",
	commands=[
		(
			'set -eu; '
			'if ! uname -r | grep -q -- "-pve"; then '
			'  echo "Skipping Proxmox VE package installation until the host is rebooted into a Proxmox kernel."; '
			'  exit 0; '
			'fi; '
			'echo "postfix postfix/main_mailer_type select No configuration" | debconf-set-selections; '
			'echo "postfix postfix/mailname string $(hostname -f)" | debconf-set-selections; '
			'DEBIAN_FRONTEND=noninteractive apt-get install -y proxmox-ve postfix open-iscsi chrony; '
			'DEBIAN_FRONTEND=noninteractive apt-get remove -y linux-image-amd64 "linux-image-6.12*"; '
			'DEBIAN_FRONTEND=noninteractive apt-get remove -y os-prober; '
			'update-grub; '
			'echo "Proxmox VE installation complete. Access the web UI at https://$(hostname --ip-address | awk \"{print $1}\"):8006/."'
		),
	],
	_sudo=True,
)


logger.info(
	"This deploy follows the Debian 13 Trixie Proxmox VE flow and directs ARM hosts to PXVIRT instead."
)