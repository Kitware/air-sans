FROM kitware/trame:py3.10-glvnd

# Copy the server directory
COPY --chown=trame-user:trame-user . /local-app
COPY --chown=trame-user:trame-user .deploy /deploy

ENV TRAME_CLIENT_TYPE=vue2
RUN /opt/trame/entrypoint.sh build