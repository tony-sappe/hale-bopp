# Oauth2
# This might be better for actual SciPlatform
#    https://www.ory.sh/run-oauth2-server-open-source-api-security/
# However for my local experiments I'll use Keycloak
#  https://www.keycloak.org/getting-started/getting-started-docker


FROM jboss/keycloak

ENV DB_VENDOR h2
ENV KEYCLOAK_USER admin
ENV KEYCLOAK_PASSWORD admin

USER root
RUN mkdir -p /home/resources/keycloak/
# COPY ./keycloak/ /opt/jboss/keycloak/

# Sets up a realm with id "backend-service" in keycloak.  Two users (aiops & admin) are provided in the realm file.
# CMD ["-b 0.0.0.0", "-Dkeycloak.profile.feature.upload_scripts=enabled", "-Dkeycloak.import=/opt/jboss/keycloak/import-realm.json"]
CMD ["-b 0.0.0.0"]
USER jboss
