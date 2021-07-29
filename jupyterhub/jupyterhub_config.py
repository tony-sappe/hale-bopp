# JupyterHub configuration
#
# If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
#
#     docker volume rm jupyterhub_jupyterhub_data

import os
import sys

from jupyter_client.localinterfaces import public_ips


# Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = "/lab"

c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'


# Docker spawner
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_CONTAINER"]
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.extra_host_config = { 'network_mode': os.environ["DOCKER_NETWORK_NAME"] }
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = public_ips()[0]

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR") or "/home/jovyan"
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = "10G"


# Services
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "admin": True,
        "command": [
            sys.executable,
            "-m",
            "jupyterhub_idle_culler",
            "--timeout={}".format(os.environ["CONTAINER_IDLE_TIMEOUT"])],
    },
]
