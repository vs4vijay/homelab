import pyinfra

# Define the target host(s) where you want to run and install Magic Mirror
# hosts = ['your_host']

# Define the tasks to be executed
@pyinfra.task
def install_magic_mirror(state):
    # Install dependencies and set up Magic Mirror
    state.package.installed(
        name='curl'
    )

    state.command(
        name='Download Magic Mirror',
        # command='curl -sL https://install.magicmirror.builders | bash'
        command='echo hey'
    )

    # Add any additional tasks or configurations here

# Run the tasks on the target host(s)
pyinfra.run(
    # hosts=hosts,
    tasks=[
        install_magic_mirror,
    ]
)