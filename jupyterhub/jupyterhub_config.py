# JupyterHub configuration
#
# If you update this file, do not forget to delete the JupyterHub Docker container before restarting the service:
#
#     docker rm jupyterhub

import os
import sys

from jupyter_client.localinterfaces import public_ips
from oauthenticator.generic import GenericOAuthenticator


def construct_db_conn_string(spawner):
    username = spawner.user.name
    return f"postgres://{username}:{username}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{username}"


def construct_bucket_name(spawner):
    username = spawner.user.name
    return f"{username}"

# Reference Links
#    https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html
#    https://jupyterhub.readthedocs.io/en/stable/api/app.html


# Baseline
c.Spawner.default_url = "/lab"
c.JupyterHub.allow_named_servers = True
c.JupyterHub.named_server_limit_per_user = 3
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.JupyterHub.shutdown_on_logout = True  # Good for demo purposes. Most likely not desirable for production



class KeycloakAuthenticator(GenericOAuthenticator):
    login_service = "Keycloak SSO"
    userdata_url = os.environ["OAUTH2_USERDATA_URL"]


c.JupyterHub.authenticator_class = KeycloakAuthenticator


# Users
c.Authenticator.whitelist = set()
c.Authenticator.admin_users = {"admin"}
c.JupyterHub.admin_access = True

# Database Connection
# c.JupyterHub.db_url = f"postgresql://{os.environ['DATABASE_URL']}"


# Docker Spawner
c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_CONTAINER"]
c.DockerSpawner.prefix = "jupyterlab"
c.DockerSpawner.name_template = "jupyterlab-{username}-notebooks-{servername}"
c.DockerSpawner.remove = True  # Default: False (If True, delete containers when servers are stopped)
# c.DockerSpawner.volumes  # Default: None (Map from host file/directory to container (guest) file/directory mount point and (optionally) a mode)
# c.DockerSpawner.pre_spawn_hook  # An optional hook function that you can implement to do some bootstrapping work before the spawner starts

# Networking
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.extra_host_config = {"network_mode": os.environ["DOCKER_NETWORK_NAME"]}
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = public_ips()[0]

c.DockerSpawner.env_keep = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "BLOB_STORE_URL"]
c.DockerSpawner.environment = {
    # database_url = os.environ["DATABASE_URL"].format(os.environ)
    "DATABASE_URL": construct_db_conn_string,
    "BLOB_STORE_BUCKET": construct_bucket_name,
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
    import boto3
    import os

    client = boto3.client(
        's3',
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        endpoint_url=os.environ["BLOB_STORE_URL"]
    )
    buckets = client.list_buckets()
    for bucket in buckets["Buckets"]:
        if bucket["Name"] == username:
            break
    else:
        client.create_bucket(Bucket=username)


c.Spawner.pre_spawn_hook = hook_runner
