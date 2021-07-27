# Quasi-Enterprise JupyterHub Deployment

This project enables an aspiring person to run an example "Science Platform" suitable for astrophysics research.
If all you need is a local JupyterLab notebook with Python 3.7 and the amazing astronomy and processing libraries then this might be overkill.
However, if you want to leverage more of an ecosystem around those components with JupyterHub then this can be a springboard to launch your own work.

Spin-up a JupyterHub server with these features:
* Reverse-Proxy
* Industry-standard SSO Authentication
* SQL database for persisting configurations and for SQL-based workflows
* Mock S3 storage (future)
* Full-suite of the common Python astrophysics & astronomical libraries

Loosely based on the deployment in use at [Université de
Versailles](https://jupyter.ens.uvsq.fr/) which is described in depth in [this blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/).


### List of All-🌟 Projects making this demonstration possible
* [Docker]()
* [Keycloak]()
* [Python]()
* [Postgres]()
* [JupyterHub](https://jupyter.org/hub)


## Features


### Adapt to your needs

This deployment is ready to clone and roll on your own server. Read
the [blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/) first,
to be sure you understand the configuration.

Then, if you like, clone this repository and apply (at least) the
following changes:

- In [`.env`](.env), set the variable `HOST` to the name of the server you
  intend to host your deployment on.
- In [`reverse-proxy/traefik.toml`](reverse-proxy/traefik.toml), edit
  the paths in `certFile` and `keyFile` and point them to your own TLS
  certificates. Possibly edit the `volumes` section in the
  `reverse-proyx` service in
  [`docker-compose.yml`](docker-compose.yml).
- In
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py),
  edit the *"Authenticator"* section according to your institution
  authentication server.  If in doubt, [read
  here](https://jupyterhub.readthedocs.io/en/stable/getting-started/authenticators-users-basics.html).

Other changes you may like to make:

- Edit [`jupyterlab/Dockerfile`](jupyterlab/Dockerfile) to include the
  software you like. Do not forget to change
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py)
  accordingly, in particular the *"user data persistence"* section.

### Run!

Once you are ready, build and launch the application with

```
docker-compose build
docker-compose up -d
```

Read the [Docker Compose manual](https://docs.docker.com/compose/) to
learn how to manage your application.
