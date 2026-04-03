from pyinfra.operations import apt, server


apt.update(
	name="Update apt repositories",
	_sudo=True,
)

apt.packages(
	name="Ensure AI tooling prerequisites are installed",
	packages=[
		"ca-certificates",
		"curl",
		"ffmpeg",
		"git",
		"git-lfs",
		"jq",
		"pciutils",
		"python3",
		"python3-pip",
		"python3-venv",
		"unzip",
	],
	_sudo=True,
)

server.shell(
	name="Initialize Git LFS for the current user",
	commands=[
		"git lfs install --skip-repo",
	],
)

# server.shell(
# 	name="Install Ollama via the official installer",
# 	commands=[
# 		(
# 			"if ! command -v ollama >/dev/null 2>&1; then "
# 			"curl -fsSL https://ollama.com/install.sh -o /tmp/ollama-install.sh "
# 			"&& sh /tmp/ollama-install.sh "
# 			"&& rm -f /tmp/ollama-install.sh; "
# 			"fi"
# 		),
# 	],
# 	_sudo=True,
# )

# server.shell(
# 	name="Install Hugging Face CLI via the official installer",
# 	commands=[
# 		(
# 			'if [ ! -x "$HOME/.local/bin/hf" ]; then '
# 			'curl -LsSf https://hf.co/cli/install.sh -o /tmp/hf-install.sh '
# 			'&& bash /tmp/hf-install.sh '
# 			'&& rm -f /tmp/hf-install.sh; '
# 			'fi'
# 		),
# 	],
# )

server.shell(
	name="Install llmfit via the official installer",
	commands=[
		(
			'if [ ! -x "$HOME/.local/bin/llmfit" ]; then '
			'curl -fsSL https://llmfit.axjns.dev/install.sh -o /tmp/llmfit-install.sh '
			'&& sh /tmp/llmfit-install.sh -s -- --local '
			'&& rm -f /tmp/llmfit-install.sh; '
			'fi'
		),
	],
)

server.shell(
	name="Install OpenCode via the official installer",
	commands=[
		(
			'if [ ! -x "$HOME/.local/bin/opencode" ]; then '
			'curl -fsSL https://opencode.ai/install -o /tmp/opencode-install.sh '
			'&& XDG_BIN_DIR="$HOME/.local/bin" bash /tmp/opencode-install.sh '
			'&& rm -f /tmp/opencode-install.sh; '
			'fi'
		),
	],
)

server.shell(
	name="Install Oh My Pi via the official installer",
	commands=[
		(
			'if [ ! -x "$HOME/.local/bin/omp" ]; then '
			'curl -fsSL https://raw.githubusercontent.com/can1357/oh-my-pi/main/scripts/install.sh -o /tmp/omp-install.sh '
			'&& PI_INSTALL_DIR="$HOME/.local/bin" sh /tmp/omp-install.sh '
			'&& rm -f /tmp/omp-install.sh; '
			'fi'
		),
	],
)

server.shell(
	name="Install llama.cpp prebuilt binaries",
	commands=[
		(
			'if [ ! -x "$HOME/.local/bin/llama-cli" ]; then '
			'release_json="$(curl -fsSL https://api.github.com/repos/ggml-org/llama.cpp/releases/latest)" '
			"&& asset_url=\"$(printf '%s' \"$release_json\" | python3 -c 'import json,sys; assets=json.load(sys.stdin)[\"assets\"]; matches=[asset[\"browser_download_url\"] for asset in assets if asset[\"name\"].endswith(\"ubuntu-x64.tar.gz\")]; print(matches[0] if matches else \"\")')\" "
			'&& [ -n "$asset_url" ] '
			'&& rm -rf /tmp/llama-bin '
			'&& mkdir -p /tmp/llama-bin '
			'&& curl -fsSL "$asset_url" -o /tmp/llama.cpp.tar.gz '
			'&& tar -xzf /tmp/llama.cpp.tar.gz -C /tmp/llama-bin '
			'&& install -Dm755 "$(find /tmp/llama-bin -type f -name llama-cli | head -n 1)" "$HOME/.local/bin/llama-cli" '
			'&& install -Dm755 "$(find /tmp/llama-bin -type f -name llama-server | head -n 1)" "$HOME/.local/bin/llama-server" '
			'&& rm -rf /tmp/llama-bin /tmp/llama.cpp.tar.gz; '
			'fi'
		),
	],
)

server.shell(
	name="Ensure local AI tools are on PATH",
	commands=[
		(
			"grep -qxF 'export PATH=\"$HOME/.local/bin:$PATH\"' ~/.bashrc "
			"|| echo 'export PATH=\"$HOME/.local/bin:$PATH\"' >> ~/.bashrc"
		)
	],
)