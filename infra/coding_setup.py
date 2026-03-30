from pyinfra.operations import apt, server


apt.update(
	name="Update apt repositories",
	_sudo=True,
)


server.shell(
	name="Install uv via the official installer",
	commands=[
		(
			'if [ ! -x "$HOME/.local/bin/uv" ]; then '
			'curl -LsSf https://astral.sh/uv/install.sh -o /tmp/uv-install.sh '
			'&& env UV_NO_MODIFY_PATH=1 sh /tmp/uv-install.sh '
			'&& rm -f /tmp/uv-install.sh; '
			'fi'
		),
	],
)

server.shell(
	name="Install bun via the official installer",
	commands=[
		(
			'if [ ! -x "$HOME/.bun/bin/bun" ]; then '
			'curl -fsSL https://bun.com/install -o /tmp/bun-install.sh '
			'&& bash /tmp/bun-install.sh '
			'&& rm -f /tmp/bun-install.sh; '
			'fi'
		),
	],
)

server.shell(
	name="Ensure uv and bun are on PATH",
	commands=[
		(
			"grep -qxF 'export PATH=\"$HOME/.local/bin:$HOME/.bun/bin:$PATH\"' ~/.bashrc "
			"|| echo 'export PATH=\"$HOME/.local/bin:$HOME/.bun/bin:$PATH\"' >> ~/.bashrc"
		),
		(
			"grep -qxF 'export PATH=\"$HOME/.local/bin:$HOME/.bun/bin:$PATH\"' ~/.profile "
			"|| echo 'export PATH=\"$HOME/.local/bin:$HOME/.bun/bin:$PATH\"' >> ~/.profile"
		),
	],
)
