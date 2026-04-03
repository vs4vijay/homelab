from pyinfra.operations import apt, server


apt.update(
	name="Update apt repositories",
	_sudo=True,
)

apt.packages(
	name="Ensure Oh My Tmux prerequisites are installed",
	packages=[
		"git",
		"tmux",
	],
	_sudo=True,
)

server.shell(
	name="Install Oh My Tmux",
	commands=[
		(
			'if [ ! -d "$HOME/.tmux" ]; then '
			'git clone --depth=1 https://github.com/gpakosz/.tmux.git "$HOME/.tmux"; '
			'fi'
		),
		'ln -sfn "$HOME/.tmux/.tmux.conf" "$HOME/.tmux.conf"',
		(
			'if [ ! -f "$HOME/.tmux.conf.local" ]; then '
			'cp "$HOME/.tmux/.tmux.conf.local" "$HOME/.tmux.conf.local"; '
			'fi'
		),
	],
)

server.shell(
	name="Install mise via the official installer",
	commands=[
		(
			'if [ ! -x "$HOME/.local/bin/mise" ]; then '
			'curl -fsSL https://mise.run -o /tmp/mise-install.sh '
			'&& MISE_INSTALL_PATH="$HOME/.local/bin/mise" sh /tmp/mise-install.sh '
			'&& rm -f /tmp/mise-install.sh; '
			'fi'
		),
	],
)

server.shell(
	name="Ensure mise is configured",
	commands=[
		(
			"grep -qxF 'eval \"$(mise activate bash)\"' ~/.bashrc "
			"|| echo 'eval \"$(mise activate bash)\"' >> ~/.bashrc"
		),
	],
)
