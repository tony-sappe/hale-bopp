FROM jupyterhub/jupyterhub:1.4.2

COPY jupyterhub_config.py .

RUN pip install \
    jupyter_client==6.1.12 \
    jupyterhub-idle-culler==1.1 \
    dockerspawner==12.1.0 \
    jupyterhub-firstuseauthenticator
