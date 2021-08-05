# JupyterHub configuration
#
# If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
#
#     docker volume rm hale-bopp_jupyterhub_data

import os

# Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = "/lab"

### Authentication per https://oauthenticator.readthedocs.io/en/stable/getting-started.html
from oauthenticator.oauth2 import OAuthLoginHandler
from oauthenticator.generic import GenericOAuthenticator
from tornado.auth import OAuth2Mixin

# OAuth2 endpoints
class MyOAuthMixin(OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = 'http://localhost:8888/auth/realms/jupyterhub/protocol/openid-connect/auth'
    _OAUTH_ACCESS_TOKEN_URL = 'http://localhost:8888/auth/realms/jupyterhub/protocol/openid-connect'

class MyOAuthLoginHandler(OAuthLoginHandler, MyOAuthMixin):
    pass

# Authenticator configuration
class MyOAuthAuthenticator(GenericOAuthenticator):
    login_service = 'keycloak'
    login_handler = MyOAuthLoginHandler
    userdata_url = 'http://localhost:8888/auth/realms/jupyterhub/protocol/openid-connect/userinfo'
    token_url = 'http://localhost:8888/auth/realms/jupyterhub/protocol/openid-connect'
    oauth_callback_url = 'http://localhost:8888/auth/realms/jupyterhub/protocol/openid-connect/auth'
    client_id = 'jupyterhub'      # Your client ID and secret, as provided to you
    client_secret = '181504b4-fc17-486f-8023-be5759d4e3d6'

c.JupyterHub.authenticator_class = MyOAuthAuthenticator

# Docker spawner
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_CONTAINER"]
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ["HUB_IP"]

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
        "name": "cull_idle",
        "admin": True,
        "command": "python /srv/jupyterhub/cull_idle_servers.py --timeout=3600".split(),
    },
]
