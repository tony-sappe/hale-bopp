FROM jupyterhub/jupyterhub:1.4.2

COPY jupyterhub_config.py .

RUN pip install \
    jupyter_client \
    jupyterhub-idle-culler \
    dockerspawner==12.1.0 \
    jupyterhub-firstuseauthenticator
