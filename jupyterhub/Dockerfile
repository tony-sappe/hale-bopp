FROM jupyterhub/jupyterhub:1.4.2

COPY jupyterhub_config.py .

RUN apt-get update && apt-get install -y postgresql-client-12

RUN pip install \
    boto3 \
    psycopg2-binary \
    jupyter_client==6.1.12 \
    jupyterhub-idle-culler==1.1 \
    dockerspawner==12.1.0 \
    jupyterhub-firstuseauthenticator
