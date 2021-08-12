# Semi-Enterprise JupyterHub Deployment

Welcome to a small project that enables an aspiring person to run a
"Science Platform" suitable for astrophysics research. This might be overkill
if all you need is a local JupyterLab notebook with Python 3.7 (and the amazing
astronomy and processing libraries). However, if you want to leverage more of
an ecosystem around those components with JupyterHub then this can be a
springboard to launch your own project.

If you're looking for a large enterprise-scale JupyterHub deployment running on
Kubernetes then checkout [Zero-to-JupyterHub
with k8s](https://zero-to-jupyterhub.readthedocs.io/en/latest/index.html)

### Spin-up a JupyterHub server with these features
* Reverse-Proxy
* Industry-standard SSO Authentication
* SQL database for persistent configurations and for SQL-based workflows
* Mock S3 object store
* Full-suite of the common Python astrophysics & astronomical libraries
* Spark processing cluster (future)

Loosely based on the documented [JupyterHub
deployment](https://github.com/defeo/jupyterhub-docker/) at [Université de
Versailles](https://jupyter.ens.uvsq.fr/) which is described in depth in
[this blog post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/).

Additionally look up the official [JupyterHub Docker
Deploy](https://github.com/jupyterhub/jupyterhub-deploy-docker) for more
JupyterHub+Docker information.

### All-🌟 projects making this demonstration possible
* [Docker](https://www.docker.com)
* [Keycloak](https://www.keycloak.org)
* [Python](https://www.python.org)
* [Postgres](https://www.postgresql.org)
* [Zenko CloudServer](https://s3-server.readthedocs.io/en/latest/)
* [JupyterHub](https://jupyter.org/hub)


## Features


### Adapt to your needs

This deployment is ready for you to explore. But if you want to clone and roll
on your own server read below!


_Disclaimer: ensure you understand the well-written by outdated [blog
post](https://opendreamkit.org/2018/10/17/jupyterhub-docker/) first,
to be sure you understand the configuration._

Then, if you like, clone this repository and look into making (at least) the
following changes:

- In [`.env`](.env), set the variable `HOST` to the name of the server you
  intend to host your deployment on.
- In [`reverse-proxy/traefik.toml`](reverse-proxy/traefik.toml), edit
  the paths in `certFile` and `keyFile` and point them to your own TLS
  certificates. Possibly edit the `volumes` section in the
  `reverse-proxy` service in
  [`docker-compose.yml`](docker-compose.yml).
- In
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py),
  edit the *"Authenticator"* section according to your authentication server.
  If in doubt, [read
  here](https://jupyterhub.readthedocs.io/en/stable/getting-started/authenticators-users-basics.html).

Other changes you may like to make:

- Edit [`jupyterlab/Dockerfile`](jupyterlab/Dockerfile) to include different
  software you like. Do not forget to change
  [`jupyterhub/jupyterhub_config.py`](jupyterhub/jupyterhub_config.py)
  accordingly, in particular the *"user data persistence"* section.

## Run!

Once you are ready, build and launch the application with:

```
docker-compose build
docker-compose up -d
```
Then navigate to [jupyterhub.docker.localhost](http://jupyterhub.docker.localhost/)
(Google Chrome might work better than other browsers, YMMV)

### Pre-configured Accounts

Jupyterhub can be accessed by either registering a new user or using `super`:`super1123` to quickly access a user space
Keycloak has the following administrator: `admin`:`admin`

## Stop

```
docker-compose down
```

## More Resources

Creating this project was a labor of love. While it didn't take an obscene
amount of time, the main frustration revolved was the constant hunt for
reference documents and examples from other successful projects. In no
particular order I'll provide links to additional content and resources which
helped put all of the pieces together.

| Link | Content |
| --- |:--- |
| [CloudServer Docker hub](https://hub.docker.com/r/zenko/cloudserver/) | Docker images and README|
| [CloudServer Read the Docs](https://s3-server.readthedocs.io/en/latest/DOCKER.html) | Goldmine of CloudServer documentation under previous name of S3-Server |
| [CloudServer Github](https://github.com/scality/cloudserver) | CloudServer code in case you need to dig deeper |
| [DockerSpawner Read the Docs](https://jupyterhub-dockerspawner.readthedocs.io/en/latest/api/index.html#dockerspawner) | DockerSpawner docs (fun to debug!) |
| [DockerSpawner Github](https://github.com/jupyterhub/jupyterhub/wiki/Spawners) | DockerSpawner details |
| [JupyterHub Docker](https://github.com/jupyterhub/jupyterhub-deploy-docker) | Official reference deployment of JupyterHub with Docker |
| [JupyterHub Oauth issue thread](https://github.com/jupyterhub/oauthenticator/issues/107) | Long and confusing thread. Valuable insights to understand some issues |
| [JupyterHub Read the Docs](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html) | So much content here |
| [JupyterHub SciPy Notebooks](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook) | If you want to start with a different JupyterLab flavor, look here |
| [JupyterHub Vienna DS Group](https://github.com/viennadatasciencegroup/jupyterhub) | Another hosted JupyterHub project |
| [Keycloak blog post](https://gruchalski.com/posts/2020-09-03-keycloak-with-docker-compose/) | Keycloak and docker-compose |
| [Keycloak Medium post](https://migueldoctor.medium.com/run-keycloak-locally-using-docker-and-secure-your-apps-in-3-steps-f6c554427e54) | Keycloak running in Docker |
| [Traefik Quick Start](https://doc.traefik.io/traefik/getting-started/quick-start/) | This is really all you probably need to get Traefik working |
| [Traefik Routing](https://doc.traefik.io/traefik/routing/providers/docker/) | If you need more details on Traefik, it's probably the routing |