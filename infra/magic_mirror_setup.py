import pyinfra
from pyinfra import host, logger
from pyinfra.operations import apt, server, python, git


apt.update(
    name="Update apt repositories",
    _sudo=True,
)



# @pyinfra.task
def install_magic_mirror():
    logger.info('Installing Magic Mirror')

    
    # Install nodejs
    apt.packages(
        name="Install NodeJS",
        packages=["nodejs"],
        present=True,
        update=True,
        _sudo=True,
    )


    # Install dependencies and set up Magic Mirror
    # state.package.installed(
    #     name='docker.io'
    # )

    # git.repo(
    #     name="Clone MagicMirror",
    #     src="https://github.com/MagicMirrorOrg/MagicMirror",
    #     dest=f"/home/{host.user}/MagicMirror",
    # )

    
    result = server.shell(
        commands=["echo output"],
    )

    
    logger.info(f"Got result: {result.stdout}")

#     # Add any additional tasks or configurations here

python.call(
    name='Install MaigcMirror',
    function=install_magic_mirror,
)


server.shell(
    name='Execute some shell',
    commands=['echo "back to other operations!"'],
)

# # Run the tasks on the target host(s)
# pyinfra.run(
#     # hosts=hosts,
#     tasks=[
#         install_magic_mirror,
#     ]
# )