# This might be better for actual SciPlatform
#    https://www.ory.sh/run-oauth2-server-open-source-api-security/
# However for local experiments we'll demonstrate with Keycloak
#  https://www.keycloak.org/getting-started/getting-started-docker

FROM jboss/keycloak:15.0.0

ENV DB_VENDOR h2
ENV KEYCLOAK_USER admin
ENV KEYCLOAK_PASSWORD admin

USER root
RUN mkdir -p /home/resources/keycloak/
COPY realm.json /opt/jboss/keycloak/

# Sets up a realm with id "jupyterhub" in keycloak.
CMD ["-b 0.0.0.0", "-Dkeycloak.profile.feature.upload_scripts=enabled", "-Dkeycloak.import=/opt/jboss/keycloak/realm.json"]
USER jboss
