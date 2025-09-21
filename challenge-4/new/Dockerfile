FROM node:20-alpine

# Install required packages
RUN apk add --no-cache curl supervisor openssh bash

# Generate SSH host keys (used by ssh client to verify server)
RUN ssh-keygen -A

# Create SSH user with empty password and bash as default shell
RUN adduser -D user -s /bin/bash && \
    passwd -d user && \
    echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    mkdir -p /var/run/sshd

# alpine gimmicks :)
RUN mkdir -p /var/empty/sshd && chmod 755 /var/empty/sshd

# Copy supervisor config
COPY supervisord.conf /etc/supervisord.conf

# Copy app code
WORKDIR /app
COPY server.js /app/

ENV FLAG=Bunian{fake_but_not_actually_because_we_dont_have_remote}

EXPOSE 8080 22

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

