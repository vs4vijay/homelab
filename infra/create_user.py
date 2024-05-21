import pyinfra

@pyinfra.api.operation
def create_user(username=None):
    if not username:
        username = input("Enter username: ")

    pyinfra.api.sudo(f"useradd {username}")

# pyinfra.inventory.hosts = ["your_host"]

pyinfra.api.run(create_user)