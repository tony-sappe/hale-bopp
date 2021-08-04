# JupyterHub configuration
#
# If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
#
#     docker volume rm jupyterhub_data

import os
import sys

from jupyter_client.localinterfaces import public_ips

def construct_db_conn_string(spawner):
    username = spawner.user.name
    return f"postgres://{username}:{username}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{username}"


# Reference Links
#    https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html
#    https://jupyterhub.readthedocs.io/en/stable/api/app.html

# Baseline
c.Spawner.default_url = "/lab"
# c.JupyterHub.db_url = os.environ["DATABASE_URL"]
c.JupyterHub.allow_named_servers = True
c.JupyterHub.named_server_limit_per_user = 3
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.JupyterHub.shutdown_on_logout = True  # Good for demo purposes. Most likely not desirable for production

# Security
c.JupyterHub.admin_access = True
c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'

# Docker Spawner
c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_CONTAINER"]
c.DockerSpawner.prefix = "jupyterlab"
c.DockerSpawner.name_template = "jupyterlab-{username}-notebooks-{servername}"
c.DockerSpawner.remove = True  # Default: False (If True, delete containers when servers are stopped)
# c.DockerSpawner.volumes  # Default: None (Map from host file/directory to container (guest) file/directory mount point and (optionally) a mode)
# c.DockerSpawner.pre_spawn_hook  # An optional hook function that you can implement to do some bootstrapping work before the spawner starts

# Networking
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.extra_host_config = { 'network_mode': os.environ["DOCKER_NETWORK_NAME"] }
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = public_ips()[0]

# c.DockerSpawner.env_keep = ["DATABASE_URL"]  # This is an admin user, don't pass to notebook server
c.DockerSpawner.environment = {
    # database_url = os.environ["DATABASE_URL"].format(os.environ)
    "DATABASE_URL": construct_db_conn_string
}

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR") or "/home/jovyan"
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

# Limits and Guarentees
c.JupyterHub.concurrent_spawn_limit = 5  # Default: 100 (Max number of concurrent users that can be spawning at a time)
c.JupyterHub.active_server_limit = 10
c.Spawner.cpu_limit = 4                  # Default: None (Max number of cpu-cores a single-user notebook server is allowed to use)
c.Spawner.cpu_guarantee = 1              # Default: None (Min number of cpu-cores a single-user notebook server is guaranteed to have available)
c.Spawner.mem_limit = "10G"              # Default: None (Maximum number of bytes a single-user notebook server is allowed to use)
c.Spawner.mem_guarantee = "1G"           # Default: None (Min number of bytes a single-user notebook server is guaranteed to have available)

# Services
c.JupyterHub.services = [
    {
        "name": "idle-culler",
        "admin": True,
        "command": [
            sys.executable,
            "-m",
            "jupyterhub_idle_culler",
            f"--timeout={os.environ['CONTAINER_IDLE_TIMEOUT']}"
        ],
    },
]

# Hooks
def hook_runner(spawner):
    database_init(spawner)
    blobstore_init(spawner)


def database_init(spawner):
    username = spawner.user.name

    # BAD Practice to insert user-provided strings like this! DockerSpawner tries to replace %s
    check_user = f"SELECT * FROM pg_catalog.pg_user WHERE usename = '{username}'"
    create_user = f"CREATE USER {username} WITH PASSWORD '{username}'"
    check_db = f"SELECT * FROM pg_database WHERE datname = '{username}'"
    create_db = f"CREATE DATABASE {username} WITH OWNER = '{username}'"
    revoke_all = f"REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM {username}"
    grant_priv = f"GRANT ALL PRIVILEGES ON DATABASE {username} TO {username}"

    import psycopg2
    connection = psycopg2.connect(dsn=os.environ["DATABASE_URL"])
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(check_user)
    if not cursor.fetchone():
        cursor.execute(create_user)
    cursor.execute(check_db)
    if not cursor.fetchone():
        cursor.execute(create_db)
    cursor.execute(revoke_all)
    cursor.execute(grant_priv)

    connection.commit()
    connection.close()


def blobstore_init(spawner):
    username = spawner.user.name
    pass

c.Spawner.pre_spawn_hook = hook_runner
